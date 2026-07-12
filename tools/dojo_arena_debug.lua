-- Z1 Dojo arena-selection diagnostic
--
-- Displays:
--   $0516 = currently selected arena
--   $0518 = previous arena used by the banner
--   $0520 = banner state/timer
--   $00F8 = buttons newly pressed
--   $00FA = buttons currently held

local arenaNames = {
    [0x00] = "BLANK",
    [0x01] = "4 SHORT",
    [0x02] = "4 TALL",
    [0x03] = "MAZE",
    [0x04] = "GRID",
    [0x05] = "CHEVY",
    [0x06] = "NSU",
    [0x07] = "SINGLE 6"
}

local function bitIsSet(value, mask)
    return math.floor(value / mask) % 2 == 1
end

local function directionText(value)
    local result = ""

    if bitIsSet(value, 0x08) then
        result = result .. "U"
    end

    if bitIsSet(value, 0x04) then
        result = result .. "D"
    end

    if bitIsSet(value, 0x02) then
        result = result .. "L"
    end

    if bitIsSet(value, 0x01) then
        result = result .. "R"
    end

    if result == "" then
        result = "-"
    end

    return result
end

while true do
    local selected = memory.readbyte(0x0516)
    local previous = memory.readbyte(0x0518)
    local bannerTimer = memory.readbyte(0x0520)

    local buttonsPressed = memory.readbyte(0x00F8)
    local buttonsDown = memory.readbyte(0x00FA)

    local selectedName = arenaNames[selected] or "INVALID"
    local previousName = arenaNames[previous] or "INVALID"

    gui.text(
        8,
        8,
        string.format(
            "SELECTED: %02X  %s",
            selected,
            selectedName
        )
    )

    gui.text(
        8,
        18,
        string.format(
            "PREVIOUS: %02X  %s",
            previous,
            previousName
        )
    )

    gui.text(
        8,
        28,
        string.format(
            "BANNER:   %02X",
            bannerTimer
        )
    )

    gui.text(
        8,
        38,
        string.format(
            "PRESSED:  %02X  DIR:%s",
            buttonsPressed,
            directionText(buttonsPressed)
        )
    )

    gui.text(
        8,
        48,
        string.format(
            "HELD:     %02X  DIR:%s SEL:%s",
            buttonsDown,
            directionText(buttonsDown),
            bitIsSet(buttonsDown, 0x20) and "YES" or "NO"
        )
    )

    emu.frameadvance()
end