"""
Test exporting this tests a couple of different things:
1. calling the exporter
2. tests some of the export options that would not other be checked with the integration tests get
   checked (notably the show_hidden)
"""
import unittest
import os
import tempfile
import sys
from typing import List
import re
from itertools import chain, permutations

from contextlib import contextmanager

from systemrdl import RDLCompiler

from peakrdl_python import PythonExporter



class TestExportHidden(unittest.TestCase):
    """
    Test class for the export of hidden and force not hidden (show hidden)
    """

    test_case_path = 'tests/testcases'
    test_case_name = 'hidden_property.rdl'
    test_case_top_level = 'hidden_property'
    test_case_reg_model_cls = test_case_top_level + '_cls'

    @contextmanager
    def build_python_wrappers_and_make_instance(self, show_hidden):
        """
        Context manager to build the python wrappers for a value of show_hidden, then import them
        and clean up afterwards
        """

        # compile the code for the test
        rdlc = RDLCompiler()
        rdlc.compile_file(os.path.join(self.test_case_path, self.test_case_name))
        spec = rdlc.elaborate(top_def_name=self.test_case_top_level).top

        exporter = PythonExporter()

        with tempfile.TemporaryDirectory() as tmpdirname:
            # the temporary package, within which the real package is placed is needed to ensure
            # that there are two separate entries in the python import cache and this avoids the
            # test failing for strange reasons
            if show_hidden:
                temp_package_name = 'show_hidden'
            else:
                temp_package_name = 'hidden'
            fq_package_path = os.path.join(tmpdirname, temp_package_name)
            os.makedirs(fq_package_path)
            with open(os.path.join(fq_package_path, '__init__.py'), 'w', encoding='utf-8') as fid:
                fid.write('pass\n')

            exporter.export(node=spec,
                            path=fq_package_path,
                            asyncoutput=False,
                            delete_existing_package_content=False,
                            skip_library_copy=False,
                            skip_test_case_generation=True,
                            legacy_block_access=False,
                            show_hidden=show_hidden)

            # add the temp directory to the python path so that it can be imported from
            sys.path.append(tmpdirname)

            reg_model_module = __import__( temp_package_name + '.' + self.test_case_top_level +
                '.reg_model.' + self.test_case_top_level,
                globals(), locals(), [self.test_case_reg_model_cls], 0)
            dut_cls = getattr(reg_model_module, self.test_case_reg_model_cls)
            peakrdl_python_package = __import__(temp_package_name + '.' +
                                                self.test_case_top_level + '.lib',
                globals(), locals(), ['CallbackSet'], 0)
            callbackset_cls = getattr(peakrdl_python_package, 'NormalCallbackSet')
            dummy_operations_module = __import__(temp_package_name + '.' +
                                                 self.test_case_top_level +
                                                 '.sim_lib.dummy_callbacks',
                                    globals(), locals(), ['dummy_read', 'dummy_write'], 0)
            dummy_read = getattr(dummy_operations_module, 'dummy_read')

            # no read/write are attempted so this can yield out a version with no callbacks
            # configured
            yield dut_cls(callbacks=callbackset_cls(read_callback=dummy_read))

            sys.path.remove(tmpdirname)

    def test_hidden(self):
        """
        Simple test to make sure that the fields marks as hidden are not generated
        """
        with self.build_python_wrappers_and_make_instance(show_hidden=False) as dut:
            self.assertFalse(dut.reg_hidden_fields.property_unhidden_field.read())
            self.assertFalse(dut.reg_hidden_fields.no_property_field.read())
            with self.assertRaises(AttributeError):
                _ = dut.reg_hidden_fields.property_hidden_field.read()

    def test_show_hidden(self):
        """
        Simple test to make sure that the fields marks as hidden are generated, when show_hidden
        is set
        """
        with self.build_python_wrappers_and_make_instance(show_hidden=True) as dut:
            self.assertFalse(dut.reg_hidden_fields.property_unhidden_field.read())
            self.assertFalse(dut.reg_hidden_fields.no_property_field.read())
            self.assertFalse(dut.reg_hidden_fields.property_hidden_field.read())


class TestExportUDP(unittest.TestCase):
    """
    Tests for including the UDPs in the generated RAL
    """

    test_case_path = 'tests/testcases'
    test_case_name = 'user_defined_properties.rdl'
    test_case_top_level = 'user_defined_properties'
    test_case_reg_model_cls = test_case_top_level + '_cls'

    @contextmanager
    def build_python_wrappers_and_make_instance(self, udp_list:List[str]):
        """
        Context manager to build the python wrappers for a value of show_hidden, then import them
        and clean up afterwards
        """

        # compile the code for the test
        rdlc = RDLCompiler()
        rdlc.compile_file(os.path.join(self.test_case_path, self.test_case_name))
        spec = rdlc.elaborate(top_def_name=self.test_case_top_level).top

        exporter = PythonExporter()

        with tempfile.TemporaryDirectory() as tmpdirname:
            # the temporary package, within which the real package is placed is needed to ensure
            # that there are two separate entries in the python import cache and this avoids the
            # test failing for strange reasons
            temp_package_name = 'dir_' + str(hash('_'.join(udp_list)))
            fq_package_path = os.path.join(tmpdirname, temp_package_name)
            os.makedirs(fq_package_path)
            with open(os.path.join(fq_package_path, '__init__.py'), 'w', encoding='utf-8') as fid:
                fid.write('pass\n')

            exporter.export(node=spec,
                            path=fq_package_path,
                            asyncoutput=False,
                            delete_existing_package_content=False,
                            skip_library_copy=False,
                            skip_test_case_generation=True,
                            legacy_block_access=False,
                            user_defined_properties_to_include=udp_list)

            # add the temp directory to the python path so that it can be imported from
            sys.path.append(tmpdirname)

            reg_model_module = __import__( temp_package_name + '.' + self.test_case_top_level +
                '.reg_model.' + self.test_case_top_level,
                globals(), locals(), [self.test_case_reg_model_cls], 0)
            dut_cls = getattr(reg_model_module, self.test_case_reg_model_cls)
            peakrdl_python_package = __import__(temp_package_name + '.' +
                                                self.test_case_top_level + '.lib',
                globals(), locals(), ['CallbackSet'], 0)
            callbackset_cls = getattr(peakrdl_python_package, 'NormalCallbackSet')
            dummy_operations_module = __import__(temp_package_name + '.' +
                                                 self.test_case_top_level +
                                                 '.sim_lib.dummy_callbacks',
                                    globals(), locals(), ['dummy_read', 'dummy_write'], 0)
            dummy_read = getattr(dummy_operations_module, 'dummy_read')

            # no read/write are attempted so this can yield out a version with no callbacks
            # configured
            yield dut_cls(callbacks=callbackset_cls(read_callback=dummy_read))

            sys.path.remove(tmpdirname)

    def test_str_property(self):
        """
        Check a str property is correctly generated in all the places, this is based on a the
        systemRDL test case having set the property to the fully qualified node name
        """

        # in the code the property str_property_to_include is always sent to the fully qualified
        # node name, arrays have to have homogeneous properties in the python systemRDL compiler
        # so the array designators are not present in the UDP

        def walk_child_registers(node):
            for register in node.get_registers(unroll=True):
                self.assertIn('str_property_to_include',
                              register.udp,
                              msg=f'{register.full_inst_name} missing str_property_to_include')
                self.assertEqual(register.udp['str_property_to_include'],
                                 re.sub(r'\[\d+\]','',register.full_inst_name))
                for field in register.fields:
                    self.assertEqual(field.udp['str_property_to_include'],
                                     re.sub(r'\[\d+\]','',field.full_inst_name))

        def walk_child_sections(node):
            for section in node.get_sections(unroll=True):
                self.assertEqual(section.udp['str_property_to_include'],
                                 re.sub(r'\[\d+\]','',section.full_inst_name))
                walk_child_sections(section)
                walk_child_registers(section)

        with self.build_python_wrappers_and_make_instance(udp_list=['str_property_to_include']) as\
                dut:
            self.assertEqual(dut.udp['str_property_to_include'], dut.full_inst_name)
            walk_child_sections(dut)
            walk_child_registers(dut)

    def test_selective_property_export(self):
        """
        Check all the permutations of the available UDPs to make sure only the correct ones get
        generated in each case
        """

        full_property_list = ['bool_property_to_include',
                              'struct_property_to_include',
                              'enum_property_to_include',
                              'int_property_to_include',
                              'str_property_to_include',
                              'int_property_to_exclude']
        for udp_to_include in chain.from_iterable(
                [permutations(full_property_list, r) for r in range(len(full_property_list))]):
            with self.build_python_wrappers_and_make_instance(udp_list=list(udp_to_include)) as \
                    dut:
                for udp in full_property_list:
                    if udp in list(udp_to_include):
                        self.assertIn(udp, dut.reg_a.field_a.udp)
                    else:
                        self.assertNotIn(udp, dut.reg_a.field_a.udp)


if __name__ == '__main__':

    unittest.main()
