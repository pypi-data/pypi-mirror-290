from __future__ import annotations


def setup(app):
    from sphinx_compendia import Constituent, make_compendium

    # Basic usage:
    #   provide a topic name, display name
    #   and the names for constituents of this topic.
    rule_topic = make_compendium("rule", ["skill", "spell"], display_name="House Rules")
    app.add_domain(rule_topic)

    # A tad more advanced usage:
    #   our constituents have long names we don't want to
    #   type each time we write some description or cross-reference,
    #   hence we also manually provide shorter role aliases
    #   so the cross-referencing markup is leaner.
    world_topic = make_compendium(
        "world",
        [
            Constituent(
                "character",
                xrefrole_aliases=["npc"],
            ),
            Constituent(
                "location",
                xrefrole_aliases=["loc", "place"],
            ),
        ],
        display_name="The Mythical World of Fjordlynn",
    )
    app.add_domain(world_topic)
