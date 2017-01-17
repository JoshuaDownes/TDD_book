from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Visit homepage, attempt to submit an empty list item.
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # Browser interrupts request (HTML5), does not load the list page
        self.assertNotIn('Buy milk', self.browser.find_element_by_tag_name('body').text)

        # Tries again with some text for item, which now works
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        # Attempt to submit second blank item
        self.get_item_input_box().send_keys('\n')

        # Browser again does not comply
        self.check_for_row_in_list_table('1: Buy milk')
        rows = self.browser.find_elements_by_css_selector('#id_list_table tr')
        self.assertEqual(len(rows), 1)

        # Corrected by filling text in
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
        