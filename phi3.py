import ollama
with open("Input.txt", "r") as inputfile:                       #opens file containing the prompts
    inputs = inputfile.readlines()                              #reads the prompts from the file
for input in inputs:                                            #for loop for sending the prompts to phi3 
    phi3response = ollama.chat(                                 #runs phi3 locally through ollama
        model="phi3",
        messages=[
        {
            'role': 'user',
            'content':input,
        }],
        stream = True)
    for responses in phi3response:
        with open("Output.txt", "a") as output:                 #opens file for the responses
            output.write(responses['message']['content'])
    with open("Output.txt","a") as output:
        output.write("\n")   
inputfile.close()                                               #closes file for the prompts 
output.close()                                                  #closes file for the responses
