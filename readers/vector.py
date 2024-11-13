import geopandas as gpd

class VectorValidator:
    def __init__(self, filepath):
        self.layer_names = gpd.list_layers(filepath)['name']
        self.layers = [gpd.read_file(filepath, layer=layer) for layer in self.layer_names]

    def check_null_field(self):
        errors = []
        for i, layer in enumerate(self.layers):
            layer_name = self.layer_names[i]
            for column_name, column  in layer.items():
                if self.check_null_column_value(column):
                    errors.append(f"La capa {layer_name} en la columna {column_name} tiene un valor nulo")
                    break
        return errors

    def check_null_column_value(self, column):
        for value in column:
            if self.check_for_null_value(value):
                return True
        return False

    def check_for_null_value(self, value):
        if value is None:
            return True
        if isinstance(value, str):
            value = value.strip()
            return value
        return False

    def check_spatial_reference_consistency(self):
        first_layer = self.layers[0]
        for layer in self.layers:
            if first_layer.crs != layer.crs:
                return True
        return False

    def check_overlap(self):
        for layer in self.layers:
            spatial_index = layer.sindex
            for i, geom1 in enumerate(layer.geometry):
                possible_matches_index = list(spatial_index.intersection(geom1.bounds))
                possible_matches = layer.iloc[possible_matches_index]
                for j, geom2 in zip(possible_matches_index, possible_matches.geometry):
                    if i != j and geom1.intersects(geom2):
                        return True
        return False

    def check_gaps(self):
        for layer in self.layers:
            union_geom = layer.unary_union
            bounding_geom = union_geom.convex_hull
            gaps = bounding_geom.difference(union_geom)
            if not gaps.is_empty:
                return True
        return False
