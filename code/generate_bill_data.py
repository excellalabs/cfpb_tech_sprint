# Imports
from faker import Faker

import pandas as pd
import os
import random
from datetime import datetime, timedelta

# Bill Generation Process
# OCR software read bills in and provided a CSV of each bill, separating the lines of the bill into different rows.
# We manually assigned metadata to each separated line. Metadata included two additional columns.
#   1st Column: Bill Category. This gives us insight on what type of bill we are working with.
#   2nd Column: Line Type. This line type can be either constant_text, random_metric_text, random_nunber_for_metric_text, account_number, client_name, service_name, client_address, or service_address.

# Outside of the CSV, we also take note of the account number format. (i.e. Cell Phone may be ###-##-####, as electric may be ##### ##)
# In addition, we summarize the bill categories and provide each bill category a format for text generation.


class GenerateBillData:
    def __init__(self):
        self.new_line = "\n"
        self.new_line_2 = self.new_line + self.new_line

        # Different Text Types
        self.constant_account_number_text = []
        self.constant_address_text = []
        self.constant_bill_header_text = []
        self.constant_concat_text = []
        self.constant_date_text = []
        self.constant_general_text = []
        self.constant_header_text = []
        self.constant_intro_text = []
        self.constant_int_usage_text = []
        self.constant_misc_phrase_text = []
        self.constant_name_text = []
        self.constant_page_header_text = []
        self.constant_price_text = []
        self.constant_range_text = []
        self.unknown_text = []
        self.misc_phrase_text = ["16F to 18F", "29F to 35F", "99C to 25C", "70C to 14C"]
        self.n_documents_generated = 2500
        self.n_sentences = 500

        self.csv_path = os.getenv(
            "CSV_PATH", "../data/final_data/csvs_for_loading_data/"
        )
        self.bill_format_csv_path = os.getenv(
            "BILL_FORMAT_PATH", "../data/final_data/bill_format/"
        )

        self.write_bills_path = os.getenv(
            "WRITE_BILLS_PATH", "../data/final_data/bills/"
        )

        self.fake = Faker()

    def generate_date(self, min_year=2015, max_year=datetime.now().year):
        # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
        start = datetime(min_year, 1, 1, 00, 00, 00)
        years = max_year - min_year + 1
        end = start + timedelta(days=365 * years)

        generated_date = str(start + (end - start) * random.random())
        generated_date = generated_date[:10]

        return generated_date

    # This is for generating an account number
    def generate_account_number(self):
        random_number = str(random.randint(100000000, 999999999))

        random_number = random_number[:1] + "-" + random_number[1:]
        random_number = random_number[:6] + "-" + random_number[6:]

        return random_number

    def generate_name(self):
        return self.fake.name()

    def generate_address(self):
        return self.fake.address()

    def generate_random_date_range_text(self):
        date_range_text = self.generate_date() + " to " + self.generate_date()
        return date_range_text

    def populate_static_data(self):

        # General Text
        self.constant_general_text.append("Specific related company information.")

        for _ in range(self.n_sentences):
            self.constant_general_text.append(self.fake.sentence())

        # Misc Phrase Text
        for _ in range(self.n_sentences):
            self.misc_phrase_text.append(self.fake.sentence())

        # Intro Text
        for _ in range(self.n_sentences):
            self.constant_intro_text.append("Pepco Company")
            self.constant_intro_text.append("Verizon Wireless")
            self.constant_intro_text.append("AT&T")
            self.constant_intro_text.append("Madison Square Garden")
            self.constant_intro_text.append("Duke Energy")
            self.constant_intro_text.append("Comcast")
            self.constant_intro_text.append("Ohio Power")
            self.constant_intro_text.append("General Electric")
            self.constant_intro_text.append("Excella")
            self.constant_intro_text.append("The Washington Post")
            self.constant_intro_text.append("New York Times")
            self.constant_intro_text.append("Amazon")
            self.constant_intro_text.append("Tesla")
            self.constant_intro_text.append("Draft Kings")

    def read_csvs_and_populate_constant_text(self):
        for file_name in os.listdir(self.csv_path):
            if file_name.endswith(".csv"):
                file_path = self.csv_path + file_name
                file_to_process = pd.read_csv(file_path)

                concat_sentence = ""
                current_text_type = ""

                # Concat sentences and add to lists above.
                for index, row in file_to_process.iterrows():

                    index_number = index
                    file_name = row["filename"]
                    text = str(row["text"])
                    text_type = row["text_type"]

                    # For beginning of process. Do not change.
                    if index_number == 0 and text_type != "Variable":
                        concat_sentence = text

                    if text_type == current_text_type and text_type != "Variable":
                        concat_sentence = concat_sentence + " " + text
                    elif text_type == "ConcatText":
                        concat_sentence = text
                        self.constant_concat_text.append(concat_sentence.lstrip())
                        concat_sentence = ""
                        current_text_type = ""
                    else:
                        if current_text_type == "AccountNumberText":
                            self.constant_account_number_text.append(
                                concat_sentence.lstrip()
                            )
                            concat_sentence = ""
                            current_text_type = ""
                        elif current_text_type == "AddressText":
                            self.constant_address_text.append(concat_sentence.lstrip())
                            concat_sentence = ""
                            current_text_type = ""
                        elif current_text_type == "AddressText":
                            self.constant_address_text.append(concat_sentence.lstrip())
                            concat_sentence = ""
                            current_text_type = ""
                        elif current_text_type == "BillHeader":
                            self.constant_bill_header_text.append(
                                concat_sentence.lstrip()
                            )
                            concat_sentence = ""
                            current_text_type = ""
                        elif current_text_type == "DateText":
                            self.constant_date_text.append(concat_sentence.lstrip())
                            concat_sentence = ""
                            current_text_type = ""
                        elif current_text_type == "GeneralText":
                            self.constant_general_text.append(concat_sentence.lstrip())
                            concat_sentence = ""
                            current_text_type = ""
                        elif current_text_type == "HeaderText":
                            self.constant_header_text.append(concat_sentence.lstrip())
                            concat_sentence = ""
                            current_text_type = ""
                        elif current_text_type == "Intro":
                            self.constant_intro_text.append(concat_sentence.lstrip())
                            concat_sentence = ""
                            current_text_type = ""
                        elif current_text_type == "IntUsageText":
                            self.constant_int_usage_text.append(
                                concat_sentence.lstrip()
                            )
                            concat_sentence = ""
                            current_text_type = ""
                        elif current_text_type == "MiscPhraseText":
                            self.constant_misc_phrase_text.append(
                                concat_sentence.lstrip()
                            )
                            concat_sentence = ""
                            current_text_type = ""
                        elif current_text_type == "NameText":
                            self.constant_name_text.append(concat_sentence.lstrip())
                            concat_sentence = ""
                            current_text_type = ""
                        elif current_text_type == "PageHeader":
                            self.constant_page_header_text.append(
                                concat_sentence.lstrip()
                            )
                            concat_sentence = ""
                            current_text_type = ""
                        elif current_text_type == "PriceText":
                            self.constant_price_text.append(concat_sentence.lstrip())
                            concat_sentence = ""
                            current_text_type = ""
                        elif current_text_type == "RangeText":
                            self.constant_range_text.append(concat_sentence.lstrip())
                            concat_sentence = ""
                            current_text_type = ""
                        else:
                            self.unknown_text.append(concat_sentence.lstrip())
                            concat_sentence = ""
                            current_text_type = ""

                    # Needed to properly loop through logic up top.
                    if text_type != "Variable":
                        current_text_type = text_type
                    elif text_type == "Variable":
                        concat_sentence = ""
                        current_text_type = ""

        # Distinct out lists.
        self.constant_account_number_text = list(set(self.constant_account_number_text))
        self.constant_bill_header_text = list(set(self.constant_bill_header_text))
        self.constant_concat_text = list(set(self.constant_concat_text))
        self.constant_date_text = list(set(self.constant_date_text))
        self.constant_general_text = list(set(self.constant_general_text))
        self.constant_header_text = list(set(self.constant_header_text))
        self.constant_intro_text = list(set(self.constant_intro_text))
        self.constant_int_usage_text = list(set(self.constant_int_usage_text))
        self.constant_misc_phrase_text = list(set(self.constant_misc_phrase_text))
        self.constant_page_header_text = list(set(self.constant_page_header_text))
        self.constant_price_text = list(set(self.constant_price_text))
        self.constant_range_text = list(set(self.constant_range_text))
        self.unknown_text = list(set(self.unknown_text))

        # print(self.constant_bill_header_text)

    # Blueprint for how we will generate a bill. Returns a list of values that contains line types.
    def retrieve_bill_format_and_generate_bill(self):

        generated_bill_text = ""
        random_account_number = self.generate_account_number()
        random_name = self.generate_name()
        random_client_address = self.generate_address()
        random_service_address = self.generate_address()
        random_name_address = [random_name, random_client_address]
        file_name_for_generation = random_name + "-" + random_account_number
        file_name_for_generation = file_name_for_generation.replace(" ", "_")

        for file_name in os.listdir(self.bill_format_csv_path):
            if file_name.endswith(".csv"):
                file_path = self.bill_format_csv_path + file_name
                file_to_process = pd.read_csv(file_path)

                # Concat sentences and add to lists above.
                for index, row in file_to_process.iterrows():

                    index_number = index
                    bill_format = row["bill_format"]
                    variable_after = row["variable_after"]

                    # Bill Format
                    if bill_format == "AccountNumberText":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(self.constant_account_number_text)
                            + self.new_line_2
                        )
                    elif bill_format == "AddressText":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(self.constant_address_text)
                            + self.new_line_2
                        )
                    elif bill_format == "BillHeader":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(self.constant_bill_header_text)
                            + self.new_line_2
                        )
                    elif bill_format == "DateText":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(self.constant_date_text)
                            + self.new_line_2
                        )
                    elif bill_format == "GeneralText":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(self.constant_general_text)
                            + self.new_line_2
                        )
                    elif bill_format == "HeaderText":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(self.constant_header_text)
                            + self.new_line_2
                        )
                    elif bill_format == "InsertNewLines":
                        generated_bill_text = generated_bill_text + self.new_line_2
                    elif bill_format == "Intro":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(self.constant_intro_text)
                            + self.new_line_2
                        )
                    elif bill_format == "IntUsageText":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(self.constant_int_usage_text)
                            + self.new_line_2
                        )
                    elif bill_format == "MiscPhraseText":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(self.constant_misc_phrase_text)
                            + self.new_line_2
                        )
                    elif bill_format == "NameText":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(self.constant_name_text)
                            + self.new_line_2
                        )
                    elif bill_format == "PageHeader":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(self.constant_page_header_text)
                            + self.new_line_2
                        )
                    elif bill_format == "PriceText":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(self.constant_price_text)
                            + self.new_line_2
                        )
                    elif bill_format == "RangeText":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(self.constant_range_text)
                            + self.new_line_2
                        )
                    elif bill_format == "UnknownText":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(self.unknown_text)
                            + self.new_line_2
                        )

                    # Variable After
                    if variable_after == "account_number_text":
                        generated_bill_text = (
                            generated_bill_text
                            + random_account_number
                            + self.new_line_2
                        )
                    elif variable_after == "client_address_text":
                        generated_bill_text = (
                            generated_bill_text
                            + random_client_address
                            + self.new_line_2
                        )
                    elif variable_after == "date_range_text":
                        generated_bill_text = (
                            generated_bill_text
                            + self.generate_random_date_range_text()
                            + self.new_line_2
                        )
                    elif variable_after == "date_text":
                        generated_bill_text = (
                            generated_bill_text + self.generate_date() + self.new_line_2
                        )
                    elif variable_after == "insert_new_lines":
                        generated_bill_text = generated_bill_text + self.new_line_2
                    elif variable_after == "int_usage":
                        generated_bill_text = (
                            generated_bill_text
                            + str(random.randint(1, 9999))
                            + self.new_line_2
                        )
                    elif variable_after == "misc_phrase_text":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(self.misc_phrase_text)
                            + self.new_line_2
                        )
                    elif variable_after == "name_text":
                        generated_bill_text = (
                            generated_bill_text + random_name + self.new_line_2
                        )
                    elif variable_after == "name_text_or_address_text":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(random_name_address)
                            + self.new_line_2
                        )
                    elif variable_after == "price_text":
                        generated_bill_text = (
                            generated_bill_text
                            + str(random.uniform(0.00, 99.99))
                            + self.new_line_2
                        )
                    elif variable_after == "service_address_text":
                        generated_bill_text = (
                            generated_bill_text
                            + random_service_address
                            + self.new_line_2
                        )
                    elif variable_after == "unknown_text":
                        generated_bill_text = (
                            generated_bill_text
                            + random.choice(self.unknown_text)
                            + self.new_line_2
                        )

        with open(self.write_bills_path + file_name_for_generation + ".txt", "w+") as f:
            f.write(generated_bill_text)

    def execute_pipeline(self):
        self.read_csvs_and_populate_constant_text()
        self.populate_static_data()

        for _ in range(self.n_documents_generated):
            self.retrieve_bill_format_and_generate_bill()
