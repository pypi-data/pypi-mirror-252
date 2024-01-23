# -*- coding: utf-8 -*-
"""
Functions for computing shapes after the poles are known

Copyright 2022 National Technology & Engineering Solutions of Sandia,
LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
Government retains certain rights in this software.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from enum import Enum
import numpy as np
from ..core.sdynpy_data import TransferFunctionArray
from ..core.sdynpy_shape import shape_array
from ..core.sdynpy_coordinate import CoordinateArray
from ..signal_processing.sdynpy_complex import collapse_complex_to_real


class ShapeSelection(Enum):
    ALL = 0
    DRIVE_POINT_COEFFICIENT = 1
    PARTICIPATION_FACTOR = 2

def compute_residues(experimental_frf: TransferFunctionArray,
                     natural_frequencies: np.ndarray,
                     damping_ratios: np.ndarray,
                     real_modes: bool = False,
                     residuals: bool = True,
                     min_frequency: float = None,
                     max_frequency: float = None,
                     weighting: np.ndarray = 'uniform',
                     displacement_derivative: int = 0,
                     frequency_lines_at_resonance: int = None,
                     frequency_lines_for_residuals: int = None):
    """
    Fit residues to FRF data given frequency and damping values

    Parameters
    ----------
    experimental_frf : TransferFunctionArray
        Experimental FRF data to which modes will be fit
    natural_frequencies : np.ndarray
        Natural Frequencies (in Hz) at which modes will be fit
    damping_ratios : np.ndarray
        Damping Ratios at which modes will be fit
    real_modes : bool, optional
        If true, fit residues will be real-valued.  False allows complex modes.
        The default is False.
    residuals : bool, optional
        Use residuals in the FRF fit. The default is True.
    min_frequency : float, optional
        Minimum frequency to use in the shape fit. The default is the lowest
        frequency in the experimental FRF.
    max_frequency : float, optional
        Maximum frequency to use in the shape fit. The default is the highest
        frequency in the experimental FRF.
    weighting : np.ndarray or string, optional
        A weighting array to use to fit shapes better at specific frequencies.
        The default is weighted by the log magnitude of the FRF matrix.  Can be
        defined as 'magnitude','uniform', or an ndarray with shape identical
        to the ordinate of the experimental frfs
    displacement_derivative : int, optional
        Defines the type of data in the FRF based on the number of derivatives
        from displacement (0 - displacement, 1 - velocity, 2 - acceleration).
        The default is 0 (displacement).
    frequency_lines_at_resonance : int, optional
        Defines the number of frequency lines to look at around the specified
        natural frequencies for computing residues.  If not specified, all
        frequency lines are used for computing shapes.
    frequency_lines_for_residuals : int, optional
        Defines the number of frequency lines at the low and high frequency to
        use in computing shapes.  Only used if frequency_lines_at_resonance is
        specified.  If not specified, the lower 10% and upper 10% of frequency
        lines will be kept.

    Returns
    -------
    shape_residues : np.ndarray
        A (..., n_modes) shaped np.ndarray where ... is the shape of the input
        experimental_frf array.  There will be one residue for each experimental
        frf (reference and response) for each mode.
    synthesized_frf : TransferFunctionArray
        Transfer function array containing the analytical fits using the
        residues.
    residual_frf : TransferFunctionArray
        Transfer function array containing the residual data from the analytical
        fits.
    """
    flat_frf = experimental_frf.flatten()
    frequencies = flat_frf[0].abscissa.copy()
    if min_frequency is None:
        min_frequency = np.min(frequencies)
    if max_frequency is None:
        max_frequency = np.max(frequencies)
    abscissa_indices = np.ones(frequencies.shape, dtype=bool)
    abscissa_indices &= (frequencies >= min_frequency)
    abscissa_indices &= (frequencies <= max_frequency)
    frequencies = frequencies[abscissa_indices]
    frf_matrix = flat_frf.ordinate[:, abscissa_indices].T.copy()
    angular_frequencies = 2 * np.pi * frequencies[:, np.newaxis]
    angular_natural_frequencies = 2 * np.pi * np.array(natural_frequencies).flatten()
    damping_ratios = np.array(damping_ratios).flatten()

    # Reduce to the kept frequency lines
    if frequency_lines_at_resonance is not None:
        solve_indices = np.argmin(np.abs(angular_natural_frequencies - angular_frequencies), axis=0)
        # print(solve_indices)
        solve_indices = np.unique(
            solve_indices[:, np.newaxis] + np.arange(frequency_lines_at_resonance) - frequency_lines_at_resonance // 2)
        solve_indices = solve_indices[(solve_indices >= 0) & (
            solve_indices < angular_frequencies.size)]
        # Add the residual indices
        if residuals:
            if frequency_lines_for_residuals is None:
                low_freq_indices = np.arange(angular_frequencies.size // 10)
                high_freq_indices = angular_frequencies.size - \
                    np.arange(angular_frequencies.size // 10) - 1
            else:
                low_freq_indices = np.arange(frequency_lines_for_residuals)
                high_freq_indices = angular_frequencies.size - \
                    np.arange(frequency_lines_for_residuals) - 1
            solve_indices = np.unique(np.concatenate(
                (solve_indices, low_freq_indices, high_freq_indices)))
        kernel_indices = np.concatenate((solve_indices, solve_indices + angular_frequencies.size))
        # print(kernel_indices)

    # Set up the kernel to solve the least squares residue problem
    denominator = ((angular_natural_frequencies**2 - angular_frequencies**2)**2
                   + (2 * damping_ratios * angular_natural_frequencies * angular_frequencies)**2)
    kernel_rr = (angular_natural_frequencies**2 - angular_frequencies**2) / denominator
    kernel_ri = 2 * damping_ratios * angular_natural_frequencies * angular_frequencies / denominator
    kernel_ir = -2 * damping_ratios * angular_natural_frequencies * angular_frequencies / denominator
    kernel_ii = (angular_natural_frequencies**2 - angular_frequencies**2) / denominator
    low_frequency_residual = (-1 / angular_frequencies**2)
    high_frequency_residual = (np.ones(angular_frequencies.shape))
    zeros = np.zeros(angular_frequencies.shape)

    kernel = np.concatenate((np.concatenate((kernel_rr, kernel_ri, low_frequency_residual, zeros, high_frequency_residual, zeros), axis=-1),
                             np.concatenate((kernel_ir, kernel_ii, zeros, low_frequency_residual, zeros, high_frequency_residual), axis=-1)), axis=0)

    # print(kernel.shape)

    # Reduce kernel depending on whether or not we want real modes or complex
    # modes
    if real_modes:
        kernel[..., angular_natural_frequencies.size:2 * angular_natural_frequencies.size] = 0

    # Reduce kernel depending on whether or not we want residuals
    if not residuals:
        kernel[..., -4:] = 0

    # Perform the solution in acceleration space
    kernel *= np.tile(-angular_frequencies**2, (2, 1))
    frf_matrix *= (1j * angular_frequencies)**(2 - displacement_derivative)

    # print(kernel.shape)

    # Weighting matrix
    if isinstance(weighting, str):
        if weighting.lower() == 'uniform':
            weighting = np.ones(frf_matrix.shape)
        elif weighting.lower() == 'magnitude':
            max_frf = np.max(np.abs(frf_matrix), axis=0, keepdims=True)
            max_frf[max_frf == 0.0] = 1.0
            weighting = np.abs(frf_matrix) / max_frf
            min_weighting = np.min(weighting, axis=0, keepdims=True)
            min_weighting[min_weighting == 0] = 1
            weighting_ratio = weighting / min_weighting
            weighting_ratio[weighting_ratio == 0] = 1
            weighting = np.log10(weighting_ratio)
        else:
            raise ValueError(
                'If weighting is specified as a string, must be "uniform" or "magnitude"')

    # Now assemble the FRF matrix
    frf_matrix_to_fit = np.concatenate((frf_matrix.real,
                                        frf_matrix.imag), axis=0)

    # Now perform the weighting
    weighting = np.tile(weighting, (2, 1))
    weighted_kernel = weighting.T[..., np.newaxis] * kernel
    weighted_frf_matrix_to_fit = (weighting * frf_matrix_to_fit).T[..., np.newaxis]

    # print(weighted_kernel.shape)
    # print(weighted_frf_matrix_to_fit.shape)

    if frequency_lines_at_resonance is not None:
        weighted_kernel = weighted_kernel[:, kernel_indices]
        weighted_frf_matrix_to_fit = weighted_frf_matrix_to_fit[:, kernel_indices]

    # now solve
    residues = (np.linalg.pinv(weighted_kernel) @ weighted_frf_matrix_to_fit).squeeze().T

    frf_fit_matrix = kernel @ residues
    frf_fit_matrix = (frf_fit_matrix[:frf_fit_matrix.shape[0] // 2, :]
                      + 1j * frf_fit_matrix[frf_fit_matrix.shape[0] // 2:, :])
    output_frf = flat_frf.extract_elements(abscissa_indices)
    output_frf.ordinate = (frf_fit_matrix / (1j * angular_frequencies)
                           ** (2 - displacement_derivative)).T
    output_frf = output_frf.reshape(experimental_frf.shape)

    # Extract shape residues and residuals
    shape_residues = (residues[:angular_natural_frequencies.size]
                      + 1j * residues[angular_natural_frequencies.size:2 * angular_natural_frequencies.size])
    shape_residues = np.moveaxis(shape_residues.reshape(-1, *experimental_frf.shape), 0, -1)
    if real_modes:
        shape_residues = np.real(shape_residues)

    # Extract residuals
    residual_frf = flat_frf.extract_elements(abscissa_indices)
    residual_matrix = kernel[:, -4:] @ residues[-4:]
    residual_matrix = (residual_matrix[:residual_matrix.shape[0] // 2, :]
                       + 1j * residual_matrix[residual_matrix.shape[0] // 2:, :])
    residual_frf.ordinate = (residual_matrix / (1j * angular_frequencies)
                             ** (2 - displacement_derivative)).T
    residual_frf = residual_frf.reshape(experimental_frf.shape)

    return shape_residues, output_frf, residual_frf


def compute_shapes(natural_frequencies: np.ndarray,
                   damping_ratios: np.ndarray,
                   coordinates: CoordinateArray,
                   residue_matrix: np.ndarray,
                   shape_selection=ShapeSelection.ALL,
                   participation_factors: np.ndarray = None):
    abs_coordinates = abs(coordinates)
    sign_matrix = np.prod(coordinates.sign(), axis=-1)
    equality_matrix = np.all(abs_coordinates == abs_coordinates[..., 0, np.newaxis], axis=-1)
    drive_point_indices = np.argmax(equality_matrix, axis=0)
    residue_scales = np.array([sign_matrix[response_index, reference_index]
                               for reference_index, response_index in enumerate(drive_point_indices)])
    signed_residue_matrix = residue_matrix * residue_scales[:, np.newaxis]
    drive_point_residues = np.array([signed_residue_matrix[response_index, reference_index, :]
                                     for reference_index, response_index in enumerate(drive_point_indices)])
    negative_drive_points = np.where(drive_point_residues < 0)
    if np.isrealobj(residue_matrix) and np.any(drive_point_residues < 0):
        print('Negative Drive Point Residues Found!')
        for mode_index, reference_index in np.sort(np.array(negative_drive_points).T[..., ::-1], axis=0):
            print('  Mode {:} Reference {:}'.format(
                mode_index + 1, str(coordinates[0, reference_index, -1])))
    mode_shape_scaling = np.sqrt(np.abs(drive_point_residues) if np.isrealobj(
        residue_matrix) else drive_point_residues)
    mode_shape_matrix = signed_residue_matrix / mode_shape_scaling
    if isinstance(shape_selection, str):
        if shape_selection.lower() in ['all']:
            shape_selection = ShapeSelection.ALL
        elif shape_selection.lower() in ['drive', 'drive point', 'dp']:
            shape_selection = ShapeSelection.DRIVE_POINT_COEFFICIENT
        elif shape_selection.lower() in ['part', 'participation', 'participation factor']:
            shape_selection = ShapeSelection.PARTICIPATION_FACTOR
    if not shape_selection == ShapeSelection.ALL:
        if shape_selection == ShapeSelection.DRIVE_POINT_COEFFICIENT:
            shape_selection_indices = np.argmax(drive_point_residues, axis=0)
        elif shape_selection == ShapeSelection.PARTICIPATION_FACTOR:
            shape_selection_indices = np.argmax(np.abs(participation_factors), axis=-1)
        else:
            raise ValueError('Invalid Shape Selection Technique')
        mode_shape_matrix = np.array([mode_shape_matrix[:, reference_index, mode_index]
                                      for mode_index, reference_index in enumerate(shape_selection_indices)]).T
    else:
        shape_selection_indices = np.arange(mode_shape_matrix.shape[1])[
            :, np.newaxis] * np.ones(mode_shape_matrix.shape[2], dtype=int)
    ref_array = np.ndarray
    shapes = shape_array(coordinate=coordinates[..., 0, 0],
                         shape_matrix=np.moveaxis(mode_shape_matrix, 0, -1),
                         frequency=natural_frequencies, damping=damping_ratios,
                         comment1=coordinates[0, :, -1].string_array()[shape_selection_indices])
    return shapes, negative_drive_points

def compute_shapes_multireference(experimental_frf: TransferFunctionArray,
                                  natural_frequencies: np.ndarray,
                                  damping_ratios: np.ndarray,
                                  participation_factors: np.ndarray,
                                  real_modes: bool = False,
                                  residuals: bool = True,
                                  min_frequency: float = None,
                                  max_frequency: float = None,
                                  displacement_derivative: int = 0,
                                  frequency_lines_at_resonance: int = None,
                                  frequency_lines_for_residuals: int = None):
    """
    Computes mode shapes from multireference datasets.
    
    Uses the modal participation factor as a constraint on the mode shapes to
    solve for the shapes in one pass, rather than solving for residues and
    subsequently solving for shapes.

    Parameters
    ----------
    experimental_frf : TransferFunctionArray
        Experimental FRF data to which modes will be fit
    natural_frequencies : np.ndarray
        Natural Frequencies (in Hz) at which modes will be fit
    damping_ratios : np.ndarray
        Damping Ratios at which modes will be fit
    participation_factors : np.ndarray
        Mode participation factors from which the shapes can be computed.
        Should have shape (n_modes x n_inputs)
    real_modes : bool, optional
        Specifies whether to solve for real modes or complex modes (default).
    residuals : bool, optional
        Use residuals in the FRF fit. The default is True.
    min_frequency : float, optional
        Minimum frequency to use in the shape fit. The default is the lowest
        frequency in the experimental FRF.
    max_frequency : float, optional
        Maximum frequency to use in the shape fit. The default is the highest
        frequency in the experimental FRF.
    displacement_derivative : int, optional
        Defines the type of data in the FRF based on the number of derivatives
        from displacement (0 - displacement, 1 - velocity, 2 - acceleration).
        The default is 0 (displacement).
    frequency_lines_at_resonance : int, optional
        Defines the number of frequency lines to look at around the specified
        natural frequencies for computing residues.  If not specified, all
        frequency lines are used for computing shapes.
    frequency_lines_for_residuals : int, optional
        Defines the number of frequency lines at the low and high frequency to
        use in computing shapes.  Only used if frequency_lines_at_resonance is
        specified.  If not specified, the lower 10% and upper 10% of frequency
        lines will be kept for computing residuals.

    Raises
    ------
    ValueError
        If the FRF is not 2-dimensional with references on the columns and
        responses on the rows.

    Returns
    -------
    output_shape : ShapeArray
        ShapeArray containing the mode shapes of the system
    frfs_resynthesized : TransferFunctionArray
        FRFs resynthesized from the fit shapes and residuals
    residual_frfs : TransferFunctionArray
        FRFs resynthesized only from the residuals used in the calculation
    """
    original_coordinates = experimental_frf.coordinate
    if not experimental_frf.ndim == 2:
        raise ValueError('FRF must be shaped n_outputs x n_inputs')
    abs_coordinate = abs(original_coordinates)
    experimental_frf = experimental_frf[abs_coordinate]
    # Also need to adjust the participation factors
    participation_factors = participation_factors*np.sign(original_coordinates[0,:,1].direction)
    frequencies = experimental_frf[0,0].abscissa.copy()
    if min_frequency is None:
        min_frequency = np.min(frequencies)
    if max_frequency is None:
        max_frequency = np.max(frequencies)
    abscissa_indices = np.ones(frequencies.shape, dtype=bool)
    abscissa_indices &= (frequencies >= min_frequency)
    abscissa_indices &= (frequencies <= max_frequency)
    frequencies = frequencies[abscissa_indices]
    frf_matrix = experimental_frf.ordinate[..., abscissa_indices].copy()
    angular_frequencies = 2 * np.pi * frequencies
    angular_natural_frequencies = 2 * np.pi * np.array(natural_frequencies).flatten()
    damping_ratios = np.array(damping_ratios).flatten()
    
    # Reduce to the kept frequency lines
    if frequency_lines_at_resonance is not None:
        solve_indices = np.argmin(np.abs(angular_natural_frequencies - angular_frequencies[:,np.newaxis]), axis=0)
        # print(solve_indices)
        solve_indices = np.unique(
            solve_indices[:, np.newaxis] + np.arange(frequency_lines_at_resonance) - frequency_lines_at_resonance // 2)
        solve_indices = solve_indices[(solve_indices >= 0) & (
            solve_indices < angular_frequencies.size)]
        # Add the residual indices
        if residuals:
            if frequency_lines_for_residuals is None:
                low_freq_indices = np.arange(angular_frequencies.size // 10)
                high_freq_indices = angular_frequencies.size - \
                    np.arange(angular_frequencies.size // 10) - 1
            else:
                low_freq_indices = np.arange(frequency_lines_for_residuals)
                high_freq_indices = angular_frequencies.size - \
                    np.arange(frequency_lines_for_residuals) - 1
            solve_indices = np.unique(np.concatenate(
                (solve_indices, low_freq_indices, high_freq_indices)))
        frf_matrix = frf_matrix[...,solve_indices]
        angular_frequencies = angular_frequencies[solve_indices]
    
    if real_modes:
        denominator = angular_natural_frequencies**2 - angular_frequencies[:,np.newaxis]**2 + 2j*damping_ratios*angular_natural_frequencies*angular_frequencies[:,np.newaxis]
        l = collapse_complex_to_real(participation_factors).T
        gamma = 1/denominator[:,np.newaxis]*np.eye(l.shape[-1])
        coef = (l@gamma).reshape(-1,gamma.shape[-1])
        
        kernel = np.concatenate((coef.real,coef.imag),axis=0)
        
    else:
        # Now set up the kernel
        poles = -damping_ratios*angular_natural_frequencies + 1j*np.sqrt(1-damping_ratios**2)*angular_natural_frequencies
        poles_conj = -damping_ratios*angular_natural_frequencies - 1j*np.sqrt(1-damping_ratios**2)*angular_natural_frequencies
        
        gamma = (1/(1j*angular_frequencies[:,np.newaxis] - poles))[...,np.newaxis,:]*np.eye(poles.size)
        gamma_conj = (1/(1j*angular_frequencies[:,np.newaxis] - poles_conj))[...,np.newaxis,:]*np.eye(poles.size)
        
        l = participation_factors.T
        l_conj = l.conj()
        
        coef = (l@gamma).reshape(-1,gamma.shape[-1])
        coef_conj = (l_conj@gamma_conj).reshape(-1,gamma.shape[-1])
    
        kernel = np.block([
            [coef.real + coef_conj.real, coef_conj.imag - coef.imag],
            [coef.imag + coef_conj.imag, coef.real - coef_conj.real],
            ])
        
    if residuals:
        lr = (-np.eye(l.shape[0])/angular_frequencies[:,np.newaxis,np.newaxis]**2).reshape(-1,l.shape[0])
        ur = (np.eye(l.shape[0])*np.ones((angular_frequencies.size,1,1))).reshape(-1,l.shape[0])
        zeros = np.zeros(lr.shape)

        residual_block = np.block([[lr,zeros,ur,zeros],
                                   [zeros,lr,zeros,ur]])

        kernel = np.concatenate((kernel,residual_block),axis=-1)
        
    # Convert to accelerations to do the solve
    omega_scale_factor = np.tile(np.repeat(-angular_frequencies**2,l.shape[0]),2)
    kernel *= omega_scale_factor[:,np.newaxis]
    frf_matrix *= (1j * angular_frequencies)**(2 - displacement_derivative)
    
    # TODO: See about putting weighting in here
    
    # Now assemble the FRF matrix to fit.
    frf_to_fit = frf_matrix.transpose().reshape(-1,experimental_frf.shape[0])
    frf_to_fit = np.concatenate((frf_to_fit.real,frf_to_fit.imag),axis=0)
    
    # Solve the least squares problem
    shape_coefficients,*metrics = np.linalg.lstsq(kernel,frf_to_fit)
    
    # Extract the shapes and residues
    if real_modes:
        shapes = (shape_coefficients[:l.shape[1]]).T
    else:
        shapes = (shape_coefficients[:l.shape[1]] + 1j*shape_coefficients[l.shape[1]:2*l.shape[1]]).T
    
    reconstruction_angular_frequencies = frequencies*2*np.pi
    residual_frfs = experimental_frf.copy().extract_elements(abscissa_indices)
    if residuals:
        lr = (-np.eye(l.shape[0])/reconstruction_angular_frequencies[:,np.newaxis,np.newaxis]**2).reshape(-1,l.shape[0])
        ur = (np.eye(l.shape[0])*np.ones((reconstruction_angular_frequencies.size,1,1))).reshape(-1,l.shape[0])
        zeros = np.zeros(lr.shape)

        residual_reconstruction_block = np.block([[lr,zeros,ur,zeros],
                                                  [zeros,lr,zeros,ur]])
    
        residual_reconstruction = (residual_reconstruction_block @ shape_coefficients[-4*l.shape[0]:])
        residual_reconstruction = (residual_reconstruction[:residual_reconstruction.shape[0]//2] 
                                   + 1j*residual_reconstruction[residual_reconstruction.shape[0]//2:]).reshape(reconstruction_angular_frequencies.size,l.shape[0],-1)
        residual_frfs.ordinate = residual_reconstruction.transpose() * (1j*reconstruction_angular_frequencies)**displacement_derivative
    else:
        residual_frfs.ordinate = 0
    
    # Now we have to go in and find the scale factor to scale the shapes correctly
    drive_points = np.where(experimental_frf.response_coordinate == experimental_frf.reference_coordinate)
    if drive_points[0].size == 0:
        print('Warning, Drive Points Not Found in Dataset, Shapes are Unscaled.')
        output_shape = shape_array(abs_coordinate[:,0,0], shapes.T,
                                   angular_natural_frequencies/(2*np.pi),
                                   damping_ratios,
                                   1)
        if real_modes:
            denominator = angular_natural_frequencies**2 - reconstruction_angular_frequencies[:,np.newaxis]**2 + 2j*damping_ratios*angular_natural_frequencies*reconstruction_angular_frequencies[:,np.newaxis]
            l = collapse_complex_to_real(participation_factors).T
            gamma = 1/denominator[:,np.newaxis]*np.eye(l.shape[-1])
            coef = (l@gamma).reshape(-1,gamma.shape[-1])
            
            full_kernel = np.concatenate((coef.real,coef.imag),axis=0)
        else:
            gamma = (1/(1j*reconstruction_angular_frequencies[:,np.newaxis] - poles))[...,np.newaxis,:]*np.eye(poles.size)
            gamma_conj = (1/(1j*reconstruction_angular_frequencies[:,np.newaxis] - poles_conj))[...,np.newaxis,:]*np.eye(poles.size)
            
            l = participation_factors.T
            l_conj = l.conj()
            
            coef = (l@gamma).reshape(-1,gamma.shape[-1])
            coef_conj = (l_conj@gamma_conj).reshape(-1,gamma.shape[-1])
    
            full_kernel = np.block([
                [coef.real + coef_conj.real, coef_conj.imag - coef.imag],
                [coef.imag + coef_conj.imag, coef.real - coef_conj.real],
                ])
        reconstruction = full_kernel@shape_coefficients[:-4*l.shape[0]:]
        reconstruction = reconstruction[:reconstruction.shape[0]//2] + 1j*reconstruction[reconstruction.shape[0]//2:]
        
        frfs_resynthesized = residual_frfs.copy()
        frfs_resynthesized.ordinate += (reconstruction.reshape(frequencies.size,-1,reconstruction.shape[-1])).transpose()
    else:
        residues = l[drive_points[1]]*shapes[drive_points[0]]
        max_residue = np.argmax(residues if real_modes else abs(residues),axis=0)
        scale_pre_sqrt = l[drive_points[1]]/shapes[drive_points[0]]
        scale_pre_sqrt = scale_pre_sqrt[max_residue,np.arange(max_residue.size)]
        if real_modes:
            negative_drive_points = np.where(scale_pre_sqrt < 0)[0]
            if len(negative_drive_points) > 0:
                print('Negative Drive Point for Modes {:}'.format(negative_drive_points+1))
                print('These shapes will not be scaled correctly!')
            scale_pre_sqrt[negative_drive_points] *= -1
        shape_scaling = np.sqrt(scale_pre_sqrt)
        shape_scaling = shape_scaling
        shapes *= shape_scaling
        
        output_shape = shape_array(abs_coordinate[:,0,0], shapes.T,
                                   angular_natural_frequencies/(2*np.pi),
                                   damping_ratios,
                                   1)
        
        frfs_resynthesized = (output_shape.compute_frf(
            frequencies,
            responses = experimental_frf.response_coordinate[:,0],
            references = experimental_frf.reference_coordinate[0,:],
            displacement_derivative = displacement_derivative)
            + residual_frfs)

    frfs_resynthesized = frfs_resynthesized[original_coordinates]
    residual_frfs = residual_frfs[original_coordinates]
    
    return output_shape,frfs_resynthesized,residual_frfs