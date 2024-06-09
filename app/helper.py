import re
import json
class main_helper(object):

    def __init__(self) -> None:
        print(f"{__class__.__name__} instantiated ")
        self.timestamp_pattern =  r'(\d{4}-\d{2}-\d{2}T\d{2}):(\d{2}:\d{2}.\d{3}Z)'
    def make_complete_lines(self,lines):
        complete_lines = []
        l = ''
        for line in lines:
            # print(line)
            l +=line.strip()
            if line == "\n":
                # print(l)
                complete_lines.append(l)
                l= ''
        return complete_lines
    # Function to handle potential conversion errors (optional)
    def try_convert(self,value):
        try:
            return float(value)
        except ValueError:
            return None
    def errors_payload(self,line):
        """Extracts data from a JSON string using the provided patterns.

    Args:
        json_string: The JSON string to extract data from.

    Returns:
        A dictionary containing the extracted data or None if extraction fails.
    """
        from patterns import patterns
        for ind,pattern in enumerate(patterns["error"]):
            # print("5"*50)
            # print(f"ERROR pattern : {pattern}")
            # print(line)
            match = pattern.search(line)
            # match = re.search(pattern, line, re.DOTALL)  # Handle multiline strings
            if match:
                # print("5"*50)
                # print(f"ERROR pattern : {pattern}")
                # print(f"match : {match} with Ind: {ind}")
                data = match.group()  # Capture the matched data (inner object)
                # print(f"data : {data}")
                if '{"Name":"subBalanceDiscrapancy","Unit":"Count"}' in data:
                    return None
                data = data.replace("ERROR Subscription balance and payment balance are not in sync ","")
                data = self.add_quotes_to_keys_and_values(data)
                # print(f"after invokSe add_quotes_to_keys_and_values : {data}")
                data = self.remove_redundant_quotes_and_escape_characters(data)
                # print(f"after invokSe remove_redundant_quotes_and_escape_characters : {data}")
                # Further processing or parsing of the captured data can be done here
                return json.loads(data)
        return None
    def transactions_payload(self,line):
        """Extracts data from a JSON string using the provided patterns.

    Args:
        json_string: The JSON string to extract data from.

    Returns:
        A dictionary containing the extracted data or None if extraction fails.
    """
        from patterns import patterns
        for ind,pattern in enumerate(patterns["transaction"]):
            match = pattern.search(line)
            # match = re.search(pattern, line, re.DOTALL)  # Handle multiline strings
            if match:
                # print(f"patterns[pattern] : {pattern}")
                # print(f"match : {match} with Ind: {ind}")
                data = match.group()  # Capture the matched data (inner object)
                # print(f"data : {data}")
                data = data.replace("Start syncing the balance ","")
                data = self.add_quotes_to_keys_and_values(data)
                # print(f"after invokSe add_quotes_to_keys_and_values : {data}")
                data = self.remove_redundant_quotes_and_escape_characters(data)
                # print(f"after invokSe remove_redundant_quotes_and_escape_characters : {data}")
                # Further processing or parsing of the captured data can be done here
                return json.loads(data)

        return None
    def add_quotes_to_keys_and_values(self,s):
        s = s.replace("\\", "")
        s = s.replace("'",'"')
        s = self.replace_colons_in_timestamps(s)
        # Add quotes around keys
        s = re.sub(r'(\w+):', r'"\1":', s)
        # Add quotes around string values
        # s = re.sub(r": '([^']+)'", r': "\1"', s)
        # Add quotes around string values that are not already quoted
        # s = re.sub(r':\s*\'([^\']*)\'', r': "\1"', s)
        s = self.replace_underscores_in_timestamps(s)
        # Add quotes around unquoted string values
        # s = re.sub(r": (\w+)", r': "\1"', s)
        return s
    
    # Regular expression pattern to find and replace double quotes within values
    def replace_double_quotes_in_values(self,match):
        # Extract the content within quotes
        content = match.group()
        # Replace double quotes with single quotes
        content = content.replace('"', "'")
        return f'{content}'

    def remove_redundant_quotes_and_escape_characters(self,json_string):
        """
        Removes redundant quotes and escape characters from a potentially corrupt JSON string.

        Args:
            json_string: The input string that may contain invalid JSON formatting.

        Returns:
            A potentially corrected JSON string, or None if the string is not valid JSON
                after processing.

        Raises:
            ValueError: If the number of opening and closing quotes within the first and last
                        replacements doesnt match, indicating a potential structural issue.
        """
        count = 1
        # Remove redundant quotes and escape characters
        corrected_string = json_string
        while True:

            b_rep = corrected_string

            corrected_string = corrected_string.replace("\\", '')
            corrected_string = corrected_string.replace('""', '"')

            corrected_string = corrected_string.replace('`', '')
            corrected_string = corrected_string.replace('"{"', '{"')


            corrected_string = corrected_string.replace('"}"', '"}')

        
            corrected_string = corrected_string.replace('}"', '}')  

            corrected_string = corrected_string.replace('"}}"', '"}}')  


            corrected_string = corrected_string.replace(']}"', ']}')  

            corrected_string = corrected_string.replace('"{[', '{[')

            corrected_string = corrected_string.replace('"[{', '[{')  


            corrected_string = corrected_string.replace('}]"', '}]')  

            corrected_string = corrected_string.replace('"[', '[') 
            # corrected_string = corrected_string.replace('null', '"null"') 
            corrected_string = re.sub(r'\bundefined\b', 'null', corrected_string)

            corrected_string = corrected_string.replace(']"', ']')

            corrected_string = corrected_string.replace('"[]"', '[]')
            corrected_string = corrected_string.replace('"{}', '{}')
            # corrected_string = re.sub(r'([a-zA-Z]"[a-zA-Z])\w+', self.replace_double_quotes_in_values, corrected_string)
            corrected_string = re.sub(r'\b\w*"\w*\b', self.replace_double_quotes_in_values, corrected_string)
            # match = re.search(pattern,corrected_string)
            # if match:
            #     culprit = match.group()
            #     solution = self.correct_timestamp_in_json(corrected_string)
            #     corrected_string = corrected_string.replace(culprit, solution)

                
            # corrected_string = corrected_string.replace('"28T12', '28T12')
            # corrected_string = corrected_string.replace('50":53', '50:53')
            corrected_string = corrected_string.replace('"calo"://', '"calo://')

            corrected_string = corrected_string.replace('"{\\', "{")
            # print(f"old string : \n {b_rep}")
            # print(f"New string : \n {corrected_string}")
            if b_rep == corrected_string:
                break

        return corrected_string

    def correct_timestamp_in_json(self,json_string):
        """
        Corrects the timestamp in the JSON string by removing the incorrect ':' within the timestamp value.

        Args:
            json_string: The input string containing the JSON data.

        Returns:
            The corrected JSON string.
        """
            # Function to replace the match with the corrected format
        def replace_match(match):
            date = match.group(1)
            time = match.group(2)
            return f'''{date.replace(r'"','')}:{time.replace('"','')}Z'''
        # Define the regex pattern to find and correct the timestamp issue
        pattern = self.timestamp_pattern

        return replace_match(re.search(pattern,json_string))
    def replace_colons_in_timestamps(self,s):
        # Regex pattern to match the timestamp
        s = s.replace("\\","")
        # s = s.replace("'",'"')
        timestamp_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}T\d{2}):(\d{2}):(\d{2}\.\d{3}Z)')
    
        
        # Function to replace colons with underscores in the matched timestamp
        def replacer(match):
            return f"{match.group(1)}_{match.group(2)}_{match.group(3)}"
        
        # Replace the matched timestamps using the replacer function
        result = timestamp_pattern.sub(replacer, s)
        
        return result
    def replace_underscores_in_timestamps(self,s):
        # Regex pattern to match the timestamp
        s = s.replace("\\","")
        # s = s.replace("'",'"')
        timestamp_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}T\d{2})_(\d{2})_(\d{2}\.\d{3}Z)')
    
        
        # Function to replace colons with underscores in the matched timestamp
        def replacer(match):
            return f"{match.group(1)}:{match.group(2)}:{match.group(3)}"
        
        # Replace the matched timestamps using the replacer function
        result = timestamp_pattern.sub(replacer, s)
        
        return result
    def balance_json_string(self, json_string):
        """
        Balances the opening and closing braces and brackets in a JSON string.

        Args:
            json_string: The input JSON string that may have imbalanced braces or brackets.

        Returns:
            The corrected JSON string with balanced braces and brackets.
        """
        # Stack to keep track of braces and brackets
        stack = []
        # Dictionary to match opening and closing braces/brackets
        matches = {'{': '}', '[': ']', '(': ')'}
        # List to store the characters of the corrected string
        corrected_chars = []

        for char in json_string:
            if char in matches:
                stack.append(char)
                corrected_chars.append(char)
            elif char in matches.values():
                if stack and matches[stack[-1]] == char:
                    stack.pop()
                    corrected_chars.append(char)
                else:
                    # If no matching opening brace/bracket, skip this closing one
                    continue
            else:
                corrected_chars.append(char)
        
        # Add missing closing braces/brackets
        while stack:
            corrected_chars.append(matches[stack.pop()])

        corrected_string = ''.join(corrected_chars)

        # Check if the corrected string is valid JSON
        try:
            json.loads(corrected_string)
        except json.JSONDecodeError as e:
            print("JSON is invalid:", e)
            return None

        return corrected_string