import glob
from pathlib import Path
from yaml import safe_load
from dvh_tools.dbt_tools.generate_comments_utils import run_yml_update_in_dir, make_yml_string

def generate_comments_from_sql(*, models_path="dbt/models", docs_path="dbt/docs"):
    # run_yml_update_in_dir oppdaterer yml-filene i henhold til sql-filene
    # i.e. fjerner/legger til kolonner/modeller basert på sql-filstrukturen
    def find_project_root(current_path):
        """Recursively find the project's root directory by looking for a specific marker (e.g., '.git' folder)."""
        if (current_path / '.git').exists():
            return current_path
        else:
            return find_project_root(current_path.parent)
    project_root = find_project_root(Path(__file__).resolve())
    models_path = str(project_root / models_path) + "/"
    yaml_files = glob.glob(models_path + "**/*.yml", recursive=True)

    run_yml_update_in_dir(models_path=models_path)

    overskriv_yml_med_custom = True  # overskriving av det i yml-filene med custom_comments
    endre_bare_tomme_kommentarer = False  # endrer bare tomme kommentarer, eller alle

    column_descriptions = {}
    table_descriptions = {}


    try:  # lese custom comments
        with open(str(project_root / docs_path / "comments_custom.yml")) as f:
            custom_comments = safe_load(f)
            custom_column_comments = custom_comments["custom_column_comments"]
            custom_table_descriptions = custom_comments["custom_table_descriptions"]
    except Exception as e:
        print(e)
        print("Ha en fil med kommentarer i 'comments_custom.yml'")

    try:  # lese source_column_comments
        with open(str(project_root / docs_path / "comments_source.yml")) as f:
            source_comments = safe_load(f)
            source_column_comments = source_comments["source_column_comments"]
            source_table_descriptions = source_comments["source_table_descriptions"]
            table_descriptions.update(source_table_descriptions)
    except Exception as e:
        print(e)
        print("Fant ikke 'comments_source.yml, som skal ha kommentarer fra source'")

    # først samle inn alle kolonnenavn og beskrivelser
    kolonner_navn = []
    kolonner_kommentar = []
    for file in yaml_files:
        # hvis fila er "sources.yml", hopp over
        if "/sources.yml" in file or "/sources_with_comments.yml" in file:
            continue
        with open(file, "r") as f:
            yml = safe_load(f)
            try:
                tabeller = yml["models"]
            except KeyError:
                print(f"KeyError on 'models' in {file}")
                continue
            for t in tabeller:
                t_name = t["name"]
                t_columns = t["columns"]
                if "description" in t:
                    table_descriptions[t_name] = t["description"]
                for c in t_columns:
                    c_name = c["name"]
                    try:
                        c_description = c["description"]
                    except KeyError:
                        print(f"{c_name} har ikke felt for beskrivelse i {t_name}")
                        continue
                    if c_description is None or c_description == "":
                        # print(f"{c_name} har ingen/tom beskrivelse i {t_name}")
                        continue
                    if c_name in kolonner_navn:
                        continue  # henter kun unike kolonnenavn og første beskrivelse
                    else:
                        kolonner_navn.append(c_name)
                        kolonner_kommentar.append(c_description)
    yml_column_comments = dict(zip(kolonner_navn, kolonner_kommentar))

    # custom > yml > source
    # overskriver source_column_comments med yml_column_comments
    for col, desc in source_column_comments.items():
        column_descriptions[col] = desc
    # overskriv databasebeskrivelser med yml
    column_descriptions.update(yml_column_comments)
    # eventuelt oppdater med custom_column_comments
    if overskriv_yml_med_custom:
        column_descriptions.update(custom_column_comments)
    # legge til nye column comments
    for col, desc in custom_column_comments.items():
        column_descriptions[col] = desc
    table_descriptions.update(custom_table_descriptions)

    manglende_kommentarer = []
    # Så parse filene og smelle inn nye kommentarer
    for f in yaml_files:
        # hvis fila er "sources.yml", hopp over
        if "/sources.yml" in f or "/sources_with_comments.yml" in f:
            continue
        with open(f, "r") as file:
            yml = dict(safe_load(file))
            yml_models = False
            try:
                yml["models"].sort(key=lambda x: x["name"])
                tabeller = yml["models"]
                yml_models = True
            except KeyError:
                print(f"Ingen 'models' i .yml {f}")
                continue
            if yml_models:
                # loop over dbt modeller i yml-fila
                for i in range(len(tabeller)):
                    t_name = tabeller[i]["name"]
                    t_columns = tabeller[i]["columns"]
                    if "description" in tabeller[i]:
                        t_desc = tabeller[i]["description"]
                        if t_desc.strip() != table_descriptions[t_name].strip():
                            print(f"Endrer beskrivelse for modell {t_name}")
                            yml["models"][i]["description"] = table_descriptions[t_name]
                    # loop over kolonnene i en modell
                    for c in range(len(t_columns)):
                        c_name = t_columns[c]["name"]
                        overskriv_beskrivelse = False
                        if not endre_bare_tomme_kommentarer:
                            overskriv_beskrivelse = True
                        try:
                            c_desc = t_columns[c]["description"]
                        except KeyError:  # ingen beskrivelse av kolonnen
                            overskriv_beskrivelse = True
                            c_desc = None
                        if c_name not in column_descriptions:
                            # print(f"Fant ingen beskrivelse å bruke for {c_name}")
                            overskriv_beskrivelse = False  # får ikke overskrevet
                            if c_name not in manglende_kommentarer:
                                manglende_kommentarer.append(c_name)
                        if overskriv_beskrivelse and c_desc != column_descriptions[c_name]:
                            print(f"Endrer beskrivelse for {c_name} i {t_name}")
                            oppdatert_desc = column_descriptions[c_name]
                            yml["models"][i]["columns"][c]["description"] = oppdatert_desc

        # skriver hver enkelt .yml-fil
        with open(f, "w") as file:
            file.write(make_yml_string(yml))

    if len(manglende_kommentarer) > 0:
        print("mangler følgende kolonner i comments_custom.yml:")
        for c_name in manglende_kommentarer:
            print("   ", c_name)
