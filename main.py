import keyboard
import pymem

from offsets import dwLocalPlayer, m_iCrosshairId, dwEntityList, m_iTeamNum, dwForceAttack

process = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(process.process_handle, "client.dll").lpBaseOfDll


def main():
    shooting = False
    while True:
        player_object = process.read_int(client + dwLocalPlayer)
        if keyboard.is_pressed("shift"):
            entity = process.read_int(player_object + m_iCrosshairId)

            if 0 < entity <= 64:
                entity = process.read_int(client + dwEntityList + (entity - 1) * 0x10)
                entity_team = process.read_int(entity + m_iTeamNum)
                player_team = process.read_int(player_object + m_iTeamNum)

                if player_team != entity_team:
                    shooting = True
                    process.write_int(client + dwForceAttack, 5)

        if not keyboard.is_pressed("space") and shooting is True:
            process.write_int(client + dwForceAttack, 4)
            shooting = False


main()
