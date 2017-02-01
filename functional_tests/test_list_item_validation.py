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
        
    def test_cannot_add_duplicate_items(self):
        # User goes to home page and starts new list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')

        # Attempt to enter a duplicate item
        self.get_item_input_box().send_keys('Buy wellies\n')

        # Se error message
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")


    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a list and causes a validation error:
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Banter too thick\n')
        self.check_for_row_in_list_table('1: Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick\n')

        error = self.get_error_element()
        self.assertTrue(error.is_displayed())  

        # She starts typing in the input box to clear the error
        self.get_item_input_box().send_keys('a')

        # She is pleased to see that the error message disappears
        error = self.get_error_element()
        self.assertFalse(error.is_displayed()) 

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')