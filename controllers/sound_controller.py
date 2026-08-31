class SoundController:
    def set_volume(self, value: float):
        print(f"Setting volume to {value * 100:.0f}%")
sound_controller = SoundController()
