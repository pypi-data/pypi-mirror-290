from pyJoules.handler.csv_handler import CSVHandler

class emissionsCSVHandler(CSVHandler):
    """Adapted CSVHandler inherited from pyJoules CSVHandler to deal with added emissions data"""
    def __init__(self, filename: str):
        super().__init__(filename)

    def _gen_header(self, first_sample):
        header = super()._gen_header(first_sample)
        return header + ';emissions;region'

    def _gen_sample_line(self, sample, domain_names):
        sample_line = super()._gen_sample_line(sample, domain_names)
        emissions_string = f';{sample.total_emissions}'
        region_string = f';{sample.region}'
        return sample_line + emissions_string + region_string

