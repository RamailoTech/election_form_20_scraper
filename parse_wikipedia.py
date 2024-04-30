import csv
def add_new_columns(csv_file, new_column1, new_column2):
    rows = []

    try:
        # Read existing CSV file and store rows
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)  # Read the header row
            for row in reader:
                rows.append(row)

        # Add new columns to header
        header.append('INC_hindi_name')
        header.append('BJP_Hindi_name')

        # Add corresponding values from new_column1 and new_column2 to each row
        for i in range(len(rows)):
            rows[i].append(new_column1[i])  # Add value from new_column1
            rows[i].append(new_column2[i])  # Add value from new_column2

        # Write updated data back to the CSV file
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write updated header
            writer.writerows(rows)   # Write updated rows

        print(f"New columns 'Result' and 'Outcome' added successfully to '{csv_file}'.")
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' not found.")
    except Exception as e:
        print(f"Error occurred: {e}")

# Replace 'your_file.csv' with the path to your CSV file
csv_file_path = 'candidate_names.csv'
names = ['गुलाब सिंह कामरो', 'रमेश सिंह', 'अंबिका सिंह देव', 'खेलसाई सिंह', 'पारस नाथ राजवाड़े', 'राजकुमारी मारावी', 'डॉ. अजय तिरके', 'विजय पैकरा', 'डॉ. प्रीतम राम', 'टी. एस. सिंह देव', 'अमरजीत भगत', 'विनय कुमार भगत', 'यू डी मिंज', 'रामपुकार सिंह', 'विद्यावती सिदार', 'प्रकाश शक्रजीत नायक', 'उत्तरी जांगड़े', 'उमेश पटेल', 'लालजीत सिंह रथिया', 'फूल सिंह रथिया',
         'जय सिंह अग्रवाल', 'पुरुषोत्तम कँवर', 'दुलेश्वरी सिदार', 'डॉ॰ के के ध्रुव', 'अटल श्रीवास्तव', 'थानेश्वर साहू', 'संजीत बनर्जी', 'डॉ॰ रश्मि आशीष सिंह', 'सियाराम कौशिक', 'शैलेश पाण्डेय', 'विजय केसरवानी', 'दिलीप लहरिया', 'रघुवेंद्र सिंह', 'व्यास काश्यप', 'चरण दास मंत', 'राम कुमार यादव', 'बलेश्वर साहू', 'शेषराज हरबन्स', 'चतुरी नंद', 'देवेन्द्र बहादुर सिंह',
         'द्वारिकाधीश यादव', 'डॉ. रश्मि चंद्राकर', 'कविता प्राण लाहरे', 'संदीप साहु', 'शैलेश त्रिवेदी', 'इंद्र कुमार साओ', 'छाया वर्मा', 'पंकज शर्मा', 'विकास उपाध्याय', 'कुलदीप जुनेजा', 'महंत राम सुन्दर दास', 'शिवकुमार दहरिया', 'धनेंद्र साहु', 'अमितेश शुक्ला', 'जनक लाल ध्रुव', 'अंबिका मारकम', 'तरिणी चंद्राकर', 'ओमकार साहु', 'संगीता सिन्हा', 'अनिला भेड़िया', 'कुँवर सिंह निशाद', 'भूपेश बघेल', 'तम्राध्वज साहू', 'अरुण वोरा', 'देवेंद्र यादव', 'मुकेश चंद्राकर', 'निर्मल कोसरे', 'रवींद्र चौबे', 'आशीष कुमार छाबड़ा', 'गुरु रुद्र कुमार',
         'नीलकंठ चंद्रवंशी', 'मोहम्मद अकबर', 'यशोदा वर्मा', 'हर्षिता स्वामी बघेल', 'गिरीश देवांगन', 'दालेश्वर साहू', 'भोला राम साहू', 'इंद्राशाह मांडवी', 'रूप सिंह पोटाई', 'सावित्री मांडवी', 'शंकर धुर्वे', 'संत राम नेताम', 'मोहन मरकम', 'चंदन कश्यप', 'लाखेश्वर बघेल', 'जितिन जायसवाल', 'दीपक बाइज', 'छवींद्र महेंद्र कर्मा', 'विक्रम मांडवी', 'कवासी लाखमा']

bjpnames = ['रेणुका सिंह', 'श्याम बिहारी जायसवाल', 'भैयालाल राजवाड़े', 'भूलन सिंह मरावी', 'लक्ष्मी राजवाड़े', 'शकुंतला सिंह पोरथे', 'रामविचार नेताम', 'उदेश्वरी पैकड़ा', 'प्रबोज भिंज', 'राजेश अग्रवाल', 'राम कुमार टोप्पो', 'राईमुनि भगत', 'विष्णु देव साई', 'गोमती साई', 'सुनीति रथिया', 'ओ. पी. चौधरी', 'शिवकुमारी चौहान', 'महेश साहू', 'हरिशचंद्र रथिया', 'ननकिराम कंवर',
            'लखन लाल देवांगन', 'प्रेमचंद पटेल', 'रामदया उइके', 'प्रणव कुमार मर्पछी', 'प्रबल प्रताप सिंह जुडेव', 'अरुण साओ', 'पुन्नूलाल मोहले', 'धर्मजीत सिंह', 'धर्मलाल कौशिक', 'अमर अग्रवाल', 'सुशांत शुक्ला', 'कृष्णमुटी बंडी', 'सौरभ सिंह', 'नारायण चंदेल', 'खिलावन साहु', 'संयोगिता सिंह जुडेव', 'कृष्णकांत चंद्रा', 'संतोष लहरे', 'सरला कोसरिया', 'सम्पत अग्रवाल', 'अल्का चंद्रकर', 'योगेश्वर राजू सिन्हा', 'दिनेशलाल जगडे', 'धनीराम धिवार', 'तनकराम वर्मा', 'शिवरतन शर्मा', 'अनुज शर्मा', 'मोतीलाल साहु', 'राजेश मुनाट', 'पुरंदर मिश्र',
            'बृजमोहन अग्रवाल', 'गुरु खुशवंत साहेब', 'इंद्रकुमार साहू', 'रोहित साहू', 'गोवरधन राम मांझी', 'श्रवण मारकम', 'अजय चंद्राकर', 'रानाजना साहू', 'राकेश यादव', 'देवलाल हलवा ठाकुर', 'वीरेन्द्र साहू', 'विजय बघेल', 'ललित चंद्राकर', 'गजेंद्र यादव', 'प्रेमप्रकाश पांडेय', 'रिकेश सेन', 'डोमन कोरसेवाड़ा', 'ईश्वर साहू', 'दीपेश साहू', 'दयालदास बघेल',
            'भावना बोहरा', 'विजय शर्मा', 'विक्रांत सिंह', 'विनोद खंडेकर', 'रमन सिंह', 'भरत वर्मा', 'गीता घासी साहू', 'संजीव साहा', 'विक्रम उसेंदी', 'गौतम उइके', 'आशाराम नेताम', 'नीलकंठ टेकम', 'लता उसेंदी', 'केदार नाथ कश्यप', 'मणिराम कश्यप', 'किरण सिंह देव', 'विनायक गोयल', 'चेताराम अरामी', 'महेश गगडा', 'सोयाम मुका']

# Add new columns to the CSV file
# add_new_columns(csv_file_path, names, bjpnames)

def delete_column(csv_file, column_name):
    rows = []

    try:
        # Read existing CSV file and store rows (excluding the specified column)
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)  # Read the header row
            column_index = header.index(column_name)  # Find index of specified column

            # Filter rows to exclude the specified column
            for row in reader:
                updated_row = [value for idx, value in enumerate(row) if idx != column_index]
                rows.append(updated_row)

        # Write updated data (without the specified column) to a new CSV file
        output_file = f"new_{csv_file}"
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([col for col in header if col != column_name])  # Write updated header
            writer.writerows(rows)  # Write updated rows

        print(f"Column '{column_name}' deleted successfully. Updated CSV file: '{output_file}'")
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' not found.")
    except ValueError:
        print(f"Error: Column '{column_name}' not found in the CSV file.")
    except Exception as e:
        print(f"Error occurred: {e}")

# Replace 'your_file.csv' with the path to your CSV file
csv_file_path = 'updated_candidate_names.csv'
column_name_to_delete = 'Result'  # Specify the name of the column to delete

# Delete specified column from the CSV file
delete_column(csv_file_path, column_name_to_delete)




