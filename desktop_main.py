from streamlit_desktop_app import start_desktop_app

if __name__ == "__main__":
    start_desktop_app(
        "app.py",
        title="Aural Alchemy MIDI Generator",
        width=1400,
        height=950,
        options={
            "server.headless": True,
            "browser.gatherUsageStats": False,
            "theme.base": "dark",
        },
    )
