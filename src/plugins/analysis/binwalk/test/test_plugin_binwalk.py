from test.unit.analysis.analysis_plugin_test_class import AnalysisPluginTest

from ..code.binwalk import AnalysisPlugin
from helperFunctions.fileSystem import get_test_data_dir
from objects.file import FileObject

TEST_OUTPUT = '''
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             Microsoft executable, portable (PE)
106008        0x19E18         XML document, version: "1.0"
113771        0x1BC6B         Zip archive data, at least v2.0 to extract, compressed size: 47799, uncompressed size: 119688, name: PH1BXRM_AM_000803003938.dat
2752561       0x2A0031        Falling entropy edge (0.026681)
12226608      0xBA9030        End of Zip archive, footer length: 22
'''


class TestAnalysisPluginBinwalk(AnalysisPluginTest):
    PLUGIN_NAME = 'binwalk'

    def setUp(self):
        config = self.init_basic_config()
        # additional setup can go here
        self.analysis_plugin = AnalysisPlugin(self, config=config)

    def tearDown(self):
        super().tearDown()
        # additional tearDown can go here

    def test_signature_analysis(self):
        test_file = FileObject(file_path='{}/container/test.zip'.format(get_test_data_dir()))
        processed_file = self.analysis_plugin.process_object(test_file)
        results = processed_file.processed_analysis[self.PLUGIN_NAME]
        self.assertGreater(len(results['signature_analysis']), 0, 'no binwalk signature analysis found')
        self.assertTrue('DECIMAL' in results['signature_analysis'], 'no valid binwalk signature analysis')

    def test_entropy_graph(self):
        test_file = FileObject(file_path='{}/container/test.zip'.format(get_test_data_dir()))
        processed_file = self.analysis_plugin.process_object(test_file)
        results = processed_file.processed_analysis[self.PLUGIN_NAME]
        self.assertGreater(len(results['entropy_analysis_graph']), 0, 'no binwalk entropy graph found')

    def test_summary(self):
        summary = self.analysis_plugin._extract_summary(TEST_OUTPUT)
        self.assertCountEqual(summary, ['Microsoft executable', 'XML document', 'Zip archive data', 'End of Zip archive'])