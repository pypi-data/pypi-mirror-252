from fretboardgtr.notes_creators import ChordFromName, ScaleFromName


def test_scale_creator():
    scale = ScaleFromName(root="C", mode="Ionian").build()
    assert scale.notes == ["C", "D", "E", "F", "G", "A", "B"]


def test_chord_creator():
    chord = ChordFromName(root="C", quality="M").build()
    assert chord.notes == ["C", "E", "G"]


def test_chord_creator_fingerings():
    fingerings = (
        ChordFromName(root="C", quality="M")
        .build()
        .get_chord_fingerings(["E", "A", "D", "G", "B", "E"])
    )
    assert len(fingerings) > 1000


def test_scale_creator_position():
    scale_positions = (
        ScaleFromName(root="C", mode="Ionian")
        .build()
        .get_scale_positions(["E", "A", "D", "G", "B", "E"])
    )
    assert len(scale_positions) > 5
