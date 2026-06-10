import xml.etree.ElementTree as ET
import os

ui_path = os.path.join("tela", "login.ui")

try:
    tree = ET.parse(ui_path)
    root = tree.getroot()
    
    print("=" * 60)
    print("WIDGETS ENCONTRADOS EM LOGIN.UI:")
    print("=" * 60)
    
    # Procurar todos os widgets com attribute 'name'
    for elem in root.iter():
        if 'name' in elem.attrib:
            name = elem.attrib['name']
            tag = elem.tag
            print(f"  {tag:30} → name='{name}'")
    
    print("\n" + "=" * 60)
    print("WIDGETS ESPERADOS PELO CÓDIGO:")
    print("=" * 60)
    print("  btn_login")
    print("  txt_usuario")
    print("  txt_senha")
    
except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()
