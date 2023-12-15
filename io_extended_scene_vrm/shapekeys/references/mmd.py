
# MMD Models all tend to have unique Shapekeys and standard is maintained by many in the community (as in, MANY STANDARDS)
# And Japanese, just like English has many ways of writing things down.
# Using Following References
# https://learnmmd.com/Make-Your-First-Model-Using-Blender-by-Mae-Blythe/Make-a-Model-Part-21/index.html 
# https://www.deviantart.com/inochi-pm/art/MMD-Facial-Expressions-Chart-V2-802048879
# https://github.com/BeebzVivian/Add-MMD-ShapeKeys/

mmd_shapekeys : list[str] = [
    # Visemes
    "あ", # A small
    "あ２", # A medium
    "あ３", # A large 
    "い", # I 
    "う", # U
    "え", # E
    "お", # O
    "お小さい", # O Small
    "ん", # N 
    "ワ", # WA 
    # ------
    "喜び", # Brows Joy
    "笑い", # Brows Smile
    "怒り眉", # Brows "Getting angry"
    "真面目", # Brows Serious
    "にこり眉", # Brows Smily (Brows Up Happily)
    "困った", # Brows Trouble
    "怒り", # Brows Angry Brows
    "眉上", # Brows Up
    "眉下", # Brows Down
    "動揺", # Brows Sad
    # Eyes
    "まばたき", # Full Blink Neutral 
    "笑い", # Full Blink Smiling 
    "ウィンク" # Wink Left, (Wink) 
    "ウィンク右", # Wink Right (Wink-b) 
    "ウィンク２", # Blink Left (Wink-c) 
    "ｳｨﾝｸ２右", # Blink Right (Wink-d) 
    "ｷﾘｯ", # Focused Eyes ("Kiri-eye"/Sharpeyes)
    "はぅ", # > <  )
    "はちゅ目", # o o  
    "なごみ", # Relaxed Eyes
    "びっくり", # Wide Eyes / ha!! (as in "Ha! I WAS RIGHT" )
    "じと目", # Tired (of this) Eyes (jitoeye) 
    "悲しむ", # Mournful/Sorrow Eyes
    "星目", # Starry Eyed 
    "星目2", # Starry Eyed Alt 
    "スターライト", # StarLight (Star shine reflecte sided)
    "はぁと", # Heart Eyes
    "瞳小", #  Small Pupil
    "恐ろしい子！", # Terrified / Scary (translated as Terrified child )
    "敵意", # Hostility
    "丸い目",  # "round eye":  (Cross referenced out)
    "ｺｯﾁﾐﾝﾅ",  # "eye invert" (Cross referenced out)
    "ハイライト消", # Eye Highlight Off
    "映り込み消", # Eye Reflection Off
    # Mouth Shapes
    "∧", # Mouse 1
    "▲", # Mouse 2
    "□", # Square Open
    "ω", # "Omega" (cat face) :3
    "ω□", # "Omega" (cat face :3 + open A)
    "キッス", # Kiss  / Smoochy
    "ワアアア!", # WTF (Mouth Agape)
    "ええ？", # WTF (Mouth Agape) Alt
    "にやり", # Smirk (Niyari) 
    "にやり2", # Smirk Wide (Niyari)
    "V", # V shape
    "口上げ", # Full Mouth Down
    "口下げ", # Full Mouth Up
    "口すぼめる", # Full Mouth Inward
    "口横広げ", # Full Mouth Widen
    # Teeth
    "上歯上げ", # Raise Upper Teeth 
    "下歯下げ", # Lower Lower Teeth / Top Teeth Only (ToothBnon)
    "上歯を隠す", # Hide Upper Teeth / ToothUP
    "下歯を隠す", # Hide Lower teeth / ToothDW
    # These Seem Extra that arent really useful in VRM, so not adding them
    "左口角下げ", # Mouth Up Left
    "左口角上げ",  # Mouth Down Left
    "右口角下げ", # Mouth Up Right
    "右口角上げ" # Mouth Down Left
]