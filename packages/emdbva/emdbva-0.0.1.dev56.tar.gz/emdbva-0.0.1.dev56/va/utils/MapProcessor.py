import os
import numpy as np
from math import floor
import math
import mrcfile
from va.utils.misc import *
from va.utils.Model import *
from va.metrics.contour_level_predicator import *


class MapProcessor:
    """
        MapProcessor class contains methods deal with map processing method and model associated map processing methods
        Instance can be initialized with either full map file path or a mrcfile map object
    """

    def __init__(self, input_map=None):
        if isinstance(input_map, str):
            if os.path.isfile(input_map):
                self.map = mrcfile.open(input_map)
            else:
                self.map = None
        elif isinstance(input_map, mrcfile.mrcfile.MrcFile):
            self.map = input_map
        else:
            self.map = None

    def get_indices(self, one_coord):
        """
            Find one atom's indices corresponding to its cubic or plane
            the 8 (cubic) or 4 (plane) indices are saved in indices variable

        :param one_coord: List contains the atom coordinates in (x, y, z) order
        :return: Tuple contains two list of index: first has the 8 or 4 indices in the cubic;
                 second has the float index of the input atom
        """
        # For non-cubic or skewed density maps, they might have different apix on different axes
        zdim = self.map.header.cella.z
        znintervals = self.map.header.mz
        z_apix = zdim / znintervals

        ydim = self.map.header.cella.y
        ynintervals = self.map.header.my
        y_apix = ydim / ynintervals

        xdim = self.map.header.cella.x
        xnintervals = self.map.header.mx
        x_apix = xdim / xnintervals

        map_zsize = self.map.header.nz
        map_ysize = self.map.header.ny
        map_xsize = self.map.header.nx

        if self.map.header.cellb.alpha == self.map.header.cellb.beta == self.map.header.cellb.gamma == 90.:
            zindex = float(one_coord[2] - self.map.header.origin.z) / z_apix - self.map.header.nzstart
            yindex = float(one_coord[1] - self.map.header.origin.y) / y_apix - self.map.header.nystart
            xindex = float(one_coord[0] - self.map.header.origin.x) / x_apix - self.map.header.nxstart

        else:
            # fractional coordinate matrix
            xindex, yindex, zindex = self.matrix_indices(one_coord)

        zfloor = int(floor(zindex))
        if zfloor >= map_zsize - 1:
            zceil = zfloor
        else:
            zceil = zfloor + 1

        yfloor = int(floor(yindex))
        if yfloor >= map_ysize - 1:
            yceil = yfloor
        else:
            yceil = yfloor + 1

        xfloor = int(floor(xindex))
        if xfloor >= map_xsize - 1:
            xceil = xfloor
        else:
            xceil = xfloor + 1

        indices = np.array(np.meshgrid(np.arange(xfloor, xceil + 1), np.arange(yfloor, yceil + 1),
                                       np.arange(zfloor, zceil + 1))).T.reshape(-1, 3)
        oneindex = [xindex, yindex, zindex]

        return (indices, oneindex)

    def matrix_indices(self, onecoor):
        """
            using the fractional coordinate matrix to calculate the indices when the maps are non-orthogonal

        :param onecoor: list contains the atom coordinates in (x, y, z) order
        :return: tuple of indices in x, y, z order
        """

        # Figure out the order of the x, y, z based on crs info in the header
        apixs = self.map.voxel_size.tolist()
        angs = [self.map.header.cellb.alpha, self.map.header.cellb.beta, self.map.header.cellb.gamma]
        matrix = self.map_matrix(apixs, angs)
        result = matrix.dot(np.asarray(onecoor))
        xindex = result[0] - self.map.header.nxstart
        yindex = result[1] - self.map.header.nystart
        zindex = result[2] - self.map.header.nzstart

        return xindex, yindex, zindex

    @staticmethod
    def map_matrix(apixs, angs):
        """
            calculate the matrix to transform Cartesian coordinates to fractional coordinates
            (check the definition to see the matrix formular)

        :param apixs: array of apix/voxel size
        :param angs: array of angles in alpha, beta, gamma order
        :return: a numpy array to be used for calculated fractional coordinates
        """

        ang = (angs[0] * math.pi / 180, angs[1] * math.pi / 180, angs[2] * math.pi / 180)
        insidesqrt = 1 + 2 * math.cos(ang[0]) * math.cos(ang[1]) * math.cos(ang[2]) - \
                     math.cos(ang[0]) ** 2 - \
                     math.cos(ang[1]) ** 2 - \
                     math.cos(ang[2]) ** 2

        cellvolume = apixs[0] * apixs[1] * apixs[2] * math.sqrt(insidesqrt)

        m11 = 1 / apixs[0]
        m12 = -math.cos(ang[2]) / (apixs[0] * math.sin(ang[2]))

        m13 = apixs[1] * apixs[2] * (math.cos(ang[0]) * math.cos(ang[2]) - math.cos(ang[1])) / (
                    cellvolume * math.sin(ang[2]))
        m21 = 0
        m22 = 1 / (apixs[1] * math.sin(ang[2]))
        m23 = apixs[0] * apixs[2] * (math.cos(ang[1]) * math.cos(ang[2]) - math.cos(ang[0])) / (
                    cellvolume * math.sin(ang[2]))
        m31 = 0
        m32 = 0
        m33 = apixs[0] * apixs[1] * math.sin(ang[2]) / cellvolume
        prematrix = [[m11, m12, m13], [m21, m22, m23], [m31, m32, m33]]
        matrix = np.asarray(prematrix)

        return matrix

    def get_close_voxels_indices(self, onecoor, n):
        """
            Given onecoor, return the nearby voxels indices; radius defined by n

        :param onecoor: list contains the atom coordinates in (x, y, z) order
        :param n: a number integer of float which define radius voxel check range radius = (n*average_voxel_size)
        :return: a list of tuples of indices in (z, y, x) format to adapt to mrcfile data format
        """

        xind, yind, zind = self.get_indices(onecoor)[1]
        voxel_sizes = self.map.voxel_size.tolist()
        atom_xind = int(xind)
        atom_yind = int(yind)
        atom_zind = int(zind)

        average_voxel_size = sum(voxel_sizes) / 3.
        radius = n * average_voxel_size
        rx = int(round(radius / voxel_sizes[0]))
        ry = int(round(radius / voxel_sizes[1]))
        rz = int(round(radius / voxel_sizes[2]))

        indices = []
        for x in range(atom_xind - rx, atom_xind + rx):
            for y in range(atom_yind - ry, atom_yind + ry):
                for z in range(atom_zind - rz, atom_zind + rz):
                    d = average_voxel_size * math.sqrt(
                        (x - atom_xind) ** 2 + (y - atom_yind) ** 2 + (z - atom_zind) ** 2)
                    if d <= radius:
                        indices.append([x, y, z])
        result = [tuple(x[::-1]) for x in indices]

        return result

    def generate_mask(self, coords, radius):
        """
            Based on the coordinates, generate a mask based on the radius
            The mask based on the map initialized in the MapProcessor class

        :param coords: a list of tuples in (x, y, z) format
        :param radius: an integer or float define the radius of mask range around the coordinate
        """

        dir_name = os.path.dirname(self.map._iostream.name)
        map_name = os.path.basename(self.map._iostream.name)
        mask = np.zeros_like(self.map.data)
        for coord in coords:
            near_indices = self.get_close_voxels_indices(coord, radius)
            for ind in near_indices:
                mask[ind] = 1
        out_map = mrcfile.new(f'{dir_name}/{map_name}_residue_mask.mrc', overwrite=True)
        out_map.set_data(mask)
        out_map.voxel_size = self.map.voxel_size
        out_map.close()

    def residue_average_resolution(self, indices, mapdata=None):
        """
            given mapdata and indices, calculate the average value of these density values

        :param mapdata: numpy array of map data
        :param indices: list of tuples of (x, y, z) coordinates
        return: average value of these density values
        """

        sum_local_resolution = 0.
        if mapdata is None:
            mapdata = self.map.data
        for ind in indices:
            sum_local_resolution += mapdata[ind]

        return sum_local_resolution / len(indices)

    @staticmethod
    def save_map(map_data, output_mapname, voxel_size=1.):
        """
            save to a new map
        :param map_data: np array of map data
        :param output_mapname: full path to output map
        :param voxel: voxel size use default as 1 if not given
        """

        m = mrcfile.new(output_mapname, overwrite=True)
        m.set_data(map_data)
        m.voxel_size = voxel_size
        m.close()


    @staticmethod
    def mask_map(input_map, mask, output_mapname=None):
        """
            Mask the input map
        :param input_map: string of full path to input map
        :param mask: string of full path to mask
        :param output_mapname: full path to output map name
        """

        in_map = mrcfile.open(input_map)
        in_map_name = os.path.basename(input_map)
        in_map_data = in_map.data
        mask_map = mrcfile.open(mask)
        mask_data = mask_map.data
        mask_name = os.path.basename(mask)
        work_dir = os.path.dirname(input_map)
        if output_mapname is None:
            output_mapname = f'{work_dir}/{in_map_name}_{mask_name}_masked.map'
        if in_map_data.shape != mask_data.shape and input_map.voxel_size == mask.voxel_size:
            print(f'Map shape mismatch: {in_map_data.shape} and {mask_data.shape} or '
                  f'voxel size mismatch: {input_map.voxel_size} and {mask_data.voxel_size}')

            return None
        else:
            out_data = in_map_data * mask_data
            voxel = in_map.voxel_size
            MapProcessor.save_map(out_data, output_mapname, voxel)

            return output_mapname

    @staticmethod
    def binarized_mask(mask, map_name):
        """
            Produce a mask with 0 and 1s (for Relion mask with value > 0.5)
        :param mask: a string of full path to a mask
        :param map_name: a string of full path of primary map related to this mask
        """

        mask_map = mrcfile.open(mask)
        mask_map_data = mask_map.data > 0.5
        new_data = mask_map_data.astype(np.uint8)
        voxel_size = mask_map.voxel_size
        work_dir = os.path.dirname(os.path.dirname(os.path.dirname(mask)))
        outmap_name = f'{work_dir}/{map_name}_binarized_mask.map'
        MapProcessor.save_map(new_data, outmap_name, voxel_size)

        return outmap_name

    @staticmethod
    def predict_contour(input_map):
        """
            Given input map, predict the contour leve
        :param input_map: a string of full input map path
        :return: a float of the contour
        """

        m = mrcfile.open(input_map)
        d = m.data
        # non-cubic map use padding 0 to make it cubic
        if not all(dim == d.shape[0] for dim in d.shape):
            dim_shape = max(d.shape)
            target_shape = (dim_shape, dim_shape, dim_shape)
            d = pad_array(m.data, target_shape)
        norm_pred = calc_level_dev(d)[0]
        pred_cl = keep_three_significant_digits(float(norm_pred))

        return pred_cl


    @staticmethod
    def map_indices(input_map, contour):
        """
            Given input map and contour return all indices that correspond to the contour value larger than contour
        :param input_map: a string of full input map path
        :param contour: a float value of the contour
        :return: a list of tuples in (x, y, z)
        """
        map = mrcfile.open(input_map)

        return np.where(map.data >= contour)

    @staticmethod
    def map_minmax(map_one, map_two):
        """
            Get input map min and max value
        :param map_one(masked_raw_map): a full path of input map one
        :param map_two: a full path of input map two
        """

        masked_raw_predicted_contour = MapProcessor.predict_contour(map_one)
        all_indices = MapProcessor.map_indices(map_one, masked_raw_predicted_contour)
        local_res_map = mrcfile.open(map_two)
        all_values = local_res_map.data[all_indices]

        return np.min(all_values), np.max(all_values)


    def model_area_indices(self, input_map, model, radius=3):
        """
            Get all indices of the 'mask' that used for the area around the model in the map
        """
        map = MapProcessor(input_map)
        # use for generate mask for the whole model or the voxels involved
        all_indices = set()
        # all_coordinates = []
        for chain in model.get_chains():
            for residue in chain.get_residues():
                residue_atom_count = 0
                for atom in residue.get_atoms():
                    if atom.name.startswith('H') or atom.get_parent().resname == 'HOH':
                        continue
                    one_coordinate = atom.coord
                    around_indices = map.get_close_voxels_indices(one_coordinate, radius)
                    # use for generate mask for the whole model or the voxels involved
                    # all_coordinates.append(one_coordinate)
                    all_indices.update(around_indices)
                if residue_atom_count == 0:
                    continue


        return all_indices, len(all_indices)



    def model_ratio(self, input_map, model, radius=3):
        """
            Check the percentage of a model that covered the input map
        :param input_map: a string of full input map path
        :param model: a string of full model path
        :param radius: distance to the atom which defined the model area, default as 3
        """

        work_dir = None

        if isinstance(input_map, str):
            work_dir = os.path.dirname(input_map)
        elif isinstance(input_map, mrcfile.mrcfile.MrcFile):
            input_map = input_map._iostream.name
            work_dir = os.path.dirname(input_map)
        model_container = Model(model, work_dir)
        # model_container = Model('/Users/zhe/Downloads/tests/VA/nfs/msd/work2/emdb/development/staging/em/81/8117/va/5irx.cif')
        loaded_model = model_container.final_model()
        model_area_indices, model_area_indices_number = self.model_area_indices(input_map, loaded_model, radius)
        ## code for model area into a map
        # mask = np.zeros_like(self.map.data)
        # for i in model_area_indices:
        #     mask[i] = 1
        # out_map = mrcfile.new(f'{work_dir}/model_area.mrc', overwrite=True)
        # out_map.set_data(mask)
        # out_map.voxel_size = self.map.voxel_size
        # out_map.close()
        ##
        predicated_contour_level = self.predict_contour(input_map)
        map_area = self.map_indices(input_map, predicated_contour_level)
        map_area_indices = list(zip(map_area[0], map_area[1], map_area[2]))
        overlapped_area = set(map_area_indices) & set(model_area_indices)
        overlapped_area_size = len(list(overlapped_area))
        # ### code for put overlap region as a map
        # mask = np.zeros_like(self.map.data)
        # for i in overlapped_area:
        #     mask[i] = 1
        # out_map = mrcfile.new(f'{work_dir}/overlap.mrc', overwrite=True)
        # out_map.set_data(mask)
        # out_map.voxel_size = self.map.voxel_size
        # out_map.close()
        # ##
        overlap_to_model = keep_three_significant_digits(overlapped_area_size/model_area_indices_number)
        overlap_to_map = keep_three_significant_digits(overlapped_area_size/len(map_area_indices))
        model_to_map = keep_three_significant_digits(model_area_indices_number/len(map_area_indices))
        print(f'overlap/model: {overlap_to_model}')
        print(f'overlap/map: {overlap_to_map}')
        print(f'model/map: {model_to_map}')
        final_result = {'model_map_ratio': {'overlap_to_model': overlap_to_model, 'overlap_to_map': overlap_to_map,
                                            'model_to_map': model_to_map}}
        out_file = f'{work_dir}/{os.path.basename(input_map)}_modelmapratio.json'
        out_json(final_result, out_file)

        return out_file






