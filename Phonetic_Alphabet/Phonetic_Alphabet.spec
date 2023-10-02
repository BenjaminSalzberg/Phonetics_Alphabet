# -*- mode: python -*-

block_cipher = None


a = Analysis(['Phonetic_Alphabet.py'],
             pathex=['./'],
             binaries=[],
             datas=[
             ('Settings.json', '.'),
             ('Alphabet_Y_Both.json', '.'),
             ('Alphabet_Y_Consonant.json', '.'),
             ('Alphabet_Y_Vowel.json', '.'),
             ('Consonants.json', '.'),
             ('Endings.json', '.'),
             ('Vowels.json', '.'),
             ('Phonetics.json', '.')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Phonetic_Alphabet',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Phonetic_Alphabet')
