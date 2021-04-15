import keyboard
import mouse
import pymem

from offsets import dwLocalPlayer, m_iCrosshairId, dwEntityList, m_iTeamNum, dwForceAttack

process = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(process.process_handle, "client.dll").lpBaseOfDll


def main():
    print("v1.1 Started!\n"
          "\"ALT\" -- Activate")
    shooting = False
    while True:
        try:
            player_object = process.read_int(client + dwLocalPlayer)
            if keyboard.is_pressed("alt"):
                entity = process.read_int(player_object + m_iCrosshairId)

                if 0 < entity <= 64:
                    entity = process.read_int(client + dwEntityList + (entity - 1) * 0x10)
                    entity_team = process.read_int(entity + m_iTeamNum)
                    player_team = process.read_int(player_object + m_iTeamNum)

                    if player_team != entity_team:
                        mouse.click()

            if not keyboard.is_pressed("alt") and shooting is True:
                shooting = False
        except Exception as error:
            print(f"Error: {error}")


main()
