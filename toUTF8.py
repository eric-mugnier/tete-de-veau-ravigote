from striprtf.striprtf import rtf_to_text

with open('tete_de_veau_ravigote.rtf', 'r', encoding='cp1252') as f:
    rtf_content = f.read()

text = rtf_to_text(rtf_content)

with open('tete_de_veau_ravigote.txt', 'w', encoding='utf-8') as f:
    f.write(text)