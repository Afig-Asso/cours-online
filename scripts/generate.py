import os, sys
import yaml
import json


root_path = os.path.join(os.path.dirname(__file__))

filename_yaml = root_path+'/../data.yaml'
filename_json_out = root_path+'/../json/data.json'
filename_md_out = root_path+'/../README.md'


def yaml_read_file(pathname):
    assert os.path.isfile(pathname)
    with open(pathname, 'r') as fid:
        content = yaml.safe_load(fid)
    return content

def get_optional(key, data):
    if key in data:
        return data[key]
    else:
        return ''

def prettyMD_class(data, tools_data):
    out = ''
    

    title = data['Title']
    url = data['url']
    university = data['University']
    level = data['Level']
    teacher = data['Teacher']
    type = data['Type']
    topic = data['Topic']

    description_opt = get_optional('Description', data)

    duration_opt = get_optional('Duration', data)
    if duration_opt!='':
        duration_opt = ', '+duration_opt

    language_opt = get_optional('Language', data)
    if language_opt!='':
        language_opt = ' - '+language_opt
    
    tool_opt = get_optional('Tool', data)
    if tool_opt in tools_data:
        tool_url = tools_data[tool_opt]['url']
        tool_opt = f'[{tool_opt}]({tool_url})'
    if tool_opt!='':
        tool_opt = f' ({tool_opt})'
    

    out += f'* **[{title}]({url})** \n\n'
    out += f'  * Thème: {topic} \n'
    if description_opt!='':
        out += f'  * _{description_opt}_ \n'
    out += f'     * {level}, {university} \n'
    out += f'     * Format: {type}{duration_opt}{language_opt}{tool_opt} \n'
    out += f'     * Enseignant: {teacher}\n'
    
    out += '<br>\n\n'
    return out

def prettyMD(data):

    out = '# Ressources de cours disponibles en ligne en Informatique Graphique \n'
  
    out += '## Compléter la base \n'
    out += 'Pour ajouter/modifier des informations:\n'
    out += '  - Option 1 (_modif externe_): Clonez le projet, modifiez le fichier data.yaml avec vos informations, envoyez un pull-request sur github.\n'
    out += '  - Option 2 (_modif direct sur le dépot_): Envoyez un email à enseignement[at]asso-afig.fr et demandez à être ajouté aux contributeurs sur github.\n' 
    out += '  - Option 3 (_simple email_): Envoyez un email à enseignement[at]asso-afig.fr avec vos informations\n' 
    
    out += '\n\n'

    out += 'Rem. Le fichier README.md est généré automatiquement (ne le modifiez pas).\n'
    out += '  1. Modifiez la base de données: fichier **data.yaml**\n'
    out += '  2. Générez les fichiers: `python scripts/generate.py` \n'


    out += '## Listing des ressources\n\n' 
    
    tools = data['Tools']

    classes = sorted(data['Classes'], key = lambda x: str(x['Level']+x['University']).replace(' ',''), reverse=False)
    for classData in classes:
        try:
            out += prettyMD_class(classData, tools)
        except KeyError as keyError:
            print('Key '+str(keyError)+' cannot be found in entry \n', classData,'\n\n')
        except:
            print("Undefined Problem with entry ",classData)

    
    return out



if __name__ == "__main__":

    data = yaml_read_file(filename_yaml)

    # export json
    with open(filename_json_out, 'w') as json_fid:
        json.dump(data, json_fid, indent=4)

    # export pretty md
    with open(filename_md_out, 'w') as md_fid:
        mdTXT = prettyMD(data)
        md_fid.write(mdTXT)