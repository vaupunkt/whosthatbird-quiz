from flask import Flask, render_template, url_for, request
import folium
import random
import requests

app = Flask(__name__)
page = 0
birds = [None] * 4


# Load the home page
@app.route('/')
def home():
    return render_template('start.html')


def options():
    query = "q:A+grp:birds"
    # Implement different countries as options / a dropdown menu later
    # selected_options = []
    # selected_options = request.form.getlist("options")
    # print(selected_options)
    # if selected_options:
    #    option_query = '+'.join(selected_options)
    #    print(option_query)
    #    query_with_options = f"q:A+grp:birds+{option_query}"
    #    query = query_with_options  # Update the global variable query
    return query
    

@app.route('/quiz', methods=['POST'])
def quiz():
    if request.method == "POST":
        global birds
        getData(options())
        # Get the details of the four random birds
        bird1, bird2, bird3, bird4 = birds
        
        # Create a list with the four bird names in a random order
        button_names = random.sample([bird1['name'], bird2['name'], bird3['name'], bird4['name']], 4)
        
        # Get the name of the correct bird
        correct_bird_name = bird1['name']
        
        # Create a map centered on the coordinates of the correct bird
        map = folium.Map(location=[bird1['lat'], bird1['lng']], width=750, height=500, zoom_start=10, tiles='OpenStreetMap')
        # Add a marker for the correct bird
        folium.Marker(location=[bird1['lat'], bird1['lng']], popup='Location of the Sound 🪶').add_to(map)
        # Render the map to HTML
        folium_map = map._repr_html_()
        # Render the quiz template with the audio source, button names, and map coordinates
        return render_template("quiz.html", folium_map = folium_map, audio_src=bird1['file'], button1=button_names[0], button2=button_names[1], button3=button_names[2], button4=button_names[3], correct_bird_name=correct_bird_name)

    
@app.route('/check_answer', methods=['POST'])
def check_answer():
    if request.method == "POST":
        # Get the selected answer and the correct bird name from the form data
        selected_answer = request.form['answer']
        correct_bird_name = request.form['correct_bird_name']
        
        # Check if the selected answer matches the correct bird name
        if selected_answer == correct_bird_name:
            result_message = "Correct! 🎉"
        else:
            result_message = f"Incorrect. The correct answer was {correct_bird_name}. 🐦"
        
        # Render the result template with the result message
        return render_template("result.html", result_message=result_message)

    
def getData(query):
    global birds
    url = 'https://xeno-canto.org/api/2/recordings?query='
    url = url + f"+{query}"
    print(url)
    response = requests.get(url)
    recordings = response.json()
    numPages = int(recordings['numPages'])
    print(numPages)
    if numPages > 1:
        page = []
        for i in range(4):
            page.append(random.randint(1, numPages))
        for i in range(4):
            response = requests.get(url + f"&page={page[i-1]}")
            recordings = response.json()
            # Create a list of tuples with (species, name) for all the recordings in the current page
            species_names = [(rec['sp'], rec['en']) for rec in recordings['recordings']]
            # Remove duplicates from the list of tuples
            species_names = list(set(species_names))
            # Remove the species and names that have already been used for the previous birds
            for j in range(i):
                used_species = birds[j]['species']
                used_name = birds[j]['name']
                species_names = [(sp, name) for (sp, name) in species_names if sp != used_species and name != used_name]
            if not species_names:
                # If there are no remaining unique species and names in the current page, try again with a new page
                return getData()
            # Select a random (species, name) tuple from the remaining list
            species_name = random.choice(species_names)
            bird_sp = species_name[0]
            bird_name = species_name[1]
            # Find the recording with the selected (species, name) tuple
            bird_recordings = next((rec for rec in recordings['recordings'] if rec['sp'] == bird_sp and rec['en'] == bird_name), None)
            if bird_recordings:
                bird_id = bird_recordings['id']
                species = bird_recordings['sp']
                name = bird_recordings['en']
                file = bird_recordings['file']
                lat = bird_recordings['lat']
                lng = bird_recordings['lng']
                birds[i] = {'id': bird_id, 'species': species, 'name': name, 'file': file, 'lat': lat, 'lng': lng}
    else:
        species_names = [(rec['sp'], rec['en']) for rec in recordings['recordings']]
        # Remove duplicates from the list of tuples
        species_names = list(set(species_names))
        # Remove the species and names that have already been used for the previous birds
        for j in range(i):
            used_species = birds[j]['species']
            used_name = birds[j]['name']
            species_names = [(sp, name) for (sp, name) in species_names if sp != used_species and name != used_name]
        if not species_names:
            # If there are no remaining unique species and names in the current page, try again with a new page
            return getData()
        # Select a random (species, name) tuple from the remaining list
        species_name = random.choice(species_names)
        bird_sp = species_name[0]
        bird_name = species_name[1]
        # Find the recording with the selected (species, name) tuple
        bird_recordings = next((rec for rec in recordings['recordings'] if rec['sp'] == bird_sp and rec['en'] == bird_name), None)
        if bird_recordings:
            bird_id = bird_recordings['id']
            species = bird_recordings['sp']
            name = bird_recordings['en']
            file = bird_recordings['file']
            lat = bird_recordings['lat']
            lng = bird_recordings['lng']
            birds[i] = {'id': bird_id, 'species': species, 'name': name, 'file': file, 'lat': lat, 'lng': lng}
    return birds

