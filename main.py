import mysql
import tkinter as tk
import mysql.connector
from tkinter import messagebox, simpledialog, scrolledtext
from mysql.connector import Error
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('words')


# fix the response.py
# still not efficient, bot response is not complete
# need a better way to extract keywords
# fix the build_query function
# nouns extracted for ingredients_query contain "ingredient" word and should be removed !!!
# dataset is not enough, need more data OR SMOKE method to generate more data?

def create_server_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def read_query(connection, query, params = None ):
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)  # If parameters are provided, use them
        else:
            cursor.execute(query)  # If no parameters, execute query directly
        result = cursor.fetchall()  # Fetch all rows of a query result
        return result
    except Error as err:
        print(f"Error: '{err}'")  # Print any error that occurs
        return None
    finally:
        cursor.close()  # Ensure the cursor is closed after query execution


# Connect to DB
connection = create_server_connection("localhost", "root", "200426", "recipe")

# print(chatbot_response("How to cook chicken, Chef?")) # test


def extract_nouns(user_input):
    user_input = user_input.lower()  # convert to lowercase
    tokens = word_tokenize(user_input)
    tagged_tokens = pos_tag(tokens)
    # 提取所有名词
    nouns = []
    for word, tag in tagged_tokens:
        if tag.startswith('NN'):  # search for all nouns
            if word != "ingredients":  #  remove ingredients
                nouns.append(word)
                print("Noun:", word)
    return nouns


def classify_request(user_input):
    user_input = user_input.lower()  # convert to lowercase
    if "how long" in user_input or "time" in user_input.lower():
        return "query_cooking_time"  # query cooking time == 1
    elif "how to cook" in user_input or "recipe" in user_input.lower() or "make" in user_input.lower():
        return "query_recipe"  # query recipe == 2
    elif "ingredients" in user_input.lower():
        return "query_ingredients"  # query ingredients == 3
    else:
        return None


def build_query(classes, keyword):
    if classes == "query_cooking_time":
        return f"SELECT preparation_time FROM recipes WHERE recipe_name = '{keyword}'"
    elif classes == "query_recipe":
        return f"SELECT instruction FROM recipes WHERE recipe_name = '{keyword}'"
    elif classes == "query_ingredients":

        return f"SELECT ingredients.ingredient_name FROM ingredients INNER JOIN recipes ON ingredients.recipe_id = recipes.recipe_id WHERE recipes.recipe_name = '{keyword}';"
    # elif classes == "general_inquiry":
    #     return 0
    else:
        # retrive all recipe names ?
        return None


def format_results(results):
    return "\n\n".join([str(result[0]) for result in results])


def chatbot_response(user_input):

    if "/help" in user_input:
        return "You can ask me about cooking time, ingredients, or recipes for any dish."
    if "hello" in user_input.lower() or "hi" in user_input.lower():
        return "Hello, I am Overcooked, your cooking assistant! How can I help you today? Type /help to require help menu."
    # if "chicken" in user_input.lower():
    #     query = "SELECT recipe FROM recipes WHERE recipe_name = 'chicken'"
    #     result = read_query(connection, query)
    #     if result:
    #         return result[0][0]
    #     else:
    #         return "Sorry, I do not have a recipe for this dish."
    #  return "Welcome to Overcooked, your cooking assistant! Ask me about any dish."

    nouns = extract_nouns(user_input)
    if not nouns:
        return "Sorry, I do not understand your request. Plz try again"

    classes = classify_request(user_input)
    print("Classes:", classes)
    dbquery = build_query(classes, nouns[0])
    print("DB Query:", dbquery)
    if not dbquery:
        return "Sorry, I do not have information on this dish."

    if dbquery and dbquery.startswith("SELECT"):
        result = read_query(connection, dbquery)
        if result:
            return format_results(result)
        else:
            return "Sorry, I do not have information on this recipe."
    else:
        return dbquery


def start_chat():
    user_input = entry.get()
    if user_input:
        response_text.config(state='normal')
        # insert user input
        response_text.insert(tk.END, "You: " + user_input + '\n')
        # get response
        response = chatbot_response(user_input)
        # insert bots response
        # response_text.insert(tk.END, "Chef: " + response + '\n\n')
        response_text.insert(tk.END, f"Chef: {response}\n\n")

        response_text.config(state='disabled')

        entry.delete(0, tk.END)
    else:
        messagebox.showinfo("Info", "Please enter your command.")



root = tk.Tk()
root.geometry("1080x720")

root.title("Overcooked Chatbot")
entry = tk.Entry(root, width=50)
entry.pack(pady=10)
submit_button = tk.Button(root, text="Submit", command=start_chat)
submit_button.pack(pady=5)
response_text = scrolledtext.ScrolledText(root, width=120, height=40, state='disabled')
response_text.pack(pady=10)

root.mainloop()

# how to cook chocolat
# how to cook kebab
# how to cook calamari
# how long it takes to cook kebab
# what ingredients do I need to make chocolat
# what ingredients are needed to make kebab