import csv
import requests

# 英語のタイプ名を日本語に翻訳する辞書
TYPE_TRANSLATIONS = {
    "normal": "ノーマル",
    "fire": "ほのお",
    "water": "みず",
    "electric": "でんき",
    "grass": "くさ",
    "ice": "こおり",
    "fighting": "かくとう",
    "poison": "どく",
    "ground": "じめん",
    "flying": "ひこう",
    "psychic": "エスパー",
    "bug": "むし",
    "rock": "いわ",
    "ghost": "ゴースト",
    "dragon": "ドラゴン",
    "dark": "あく",
    "steel": "はがね",
    "fairy": "フェアリー",
}

def get_pokemon_data(limit=151):
    base_url = "https://pokeapi.co/api/v2/pokemon/"
    species_url = "https://pokeapi.co/api/v2/pokemon-species/"
    pokemon_data = []

    # ポケモン番号順に取得
    for i in range(1, limit + 1):
        # 基本情報（タイプなど）を取得
        response = requests.get(f"{base_url}{i}")
        if response.status_code == 200:
            pokemon = response.json()
            # タイプ情報を日本語に変換
            types = [
                TYPE_TRANSLATIONS.get(t["type"]["name"], t["type"]["name"])
                for t in pokemon["types"]
            ]

            # 日本語の名前を取得
            species_response = requests.get(f"{species_url}{i}")
            if species_response.status_code == 200:
                species_data = species_response.json()
                jp_name = next(
                    (name_entry["name"] for name_entry in species_data["names"] if name_entry["language"]["name"] == "ja"),
                    "不明"
                )
                pokemon_data.append({
                    "id": i,
                    "name": jp_name,
                    "types": types
                })
            else:
                print(f"Failed to fetch species data for Pokémon ID {i}")
        else:
            print(f"Failed to fetch data for Pokémon ID {i}")

    return pokemon_data

def save_to_csv(pokemon_list, filename="pokemon.csv"):
    with open(filename, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        # ヘッダー行を書き込み
        writer.writerow(["番号", "名前", "タイプ1", "タイプ2"])
        # データ行を書き込み
        for pokemon in pokemon_list:
            # タイプが1つしかない場合は2つ目のタイプを空欄にする
            row = [pokemon["id"], pokemon["name"]] + pokemon["types"] + [""] * (2 - len(pokemon["types"]))
            writer.writerow(row)

# データ取得
limit = 151
pokemon_list = get_pokemon_data(limit)

# CSVに保存
save_to_csv(pokemon_list, "pokemon.csv")

print("CSVファイルにデータを保存しました！")
