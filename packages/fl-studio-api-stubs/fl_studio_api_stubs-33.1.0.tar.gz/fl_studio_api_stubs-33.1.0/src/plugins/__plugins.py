"""
plugins
"""
from fl_model.decorators import since
import midi


@since(8)
def isValid(
    index: int,
    slotIndex: int = -1,
    useGlobalIndex: bool = False,
) -> bool:
    """
    Returns whether there is a valid plugin at `index`/`slotIndex`.

    ## Notes

    * Audio samples are not considered to be plugins in FL Studio.

    ## Args

    * `index` (`int`): index on channel rack or mixer.

    * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to `-1`.

    * `useGlobalIndex` (`bool`, optional): whether to use global channel
      indexes when modifying plugins on the channel rack. Defaults to `False`.

    ## Returns

    * `bool`: whether there is a valid plugin at `index`.

    Included since API version 8.

    ## API Changes

    * v26: add `useGlobalIndex` flag.
    """
    return False


@since(12)
def getPluginName(
    index: int,
    slotIndex: int = -1,
    userName: bool = False,
    useGlobalIndex: bool = False,
) -> str:
    """
    Returns the name of the plugin at `index`/slotIndex`. This returns the
    original plugin name if `userName` is `False`, otherwise the name of the
    plugin as set by the user.

    ## Args

    * `index` (`int`): index on channel rack or mixer.

    * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to `-1`.

    * `userName` (`bool`, optional): whether to return the user's name for the
      plugin (`True`), or the default name for the plugin (`False`). Defaults
      to `False`.

    * `useGlobalIndex` (`bool`, optional): whether to use global channel
      indexes when modifying plugins on the channel rack. Defaults to `False`.

    ## Returns

    * `str`: plugin name.

    Included since API version 8.

    ## API Changes

    * v12: add `userName` flag.

    * v26: add `useGlobalIndex` flag.
    """
    return ""


@since(8)
def getParamCount(
    index: int,
    slotIndex: int = -1,
    useGlobalIndex: bool = False,
) -> int:
    """
    Returns the number of parameters that a plugin has.

    ## Note

    * VST plugins are listed as having `4240` parameters, but not all of
      these are necessarily used by the plugin. The first `4096` are for
      parameters, then the next `128` are used for MIDI CC sends `0` to `127`.
      The final `16` are used for after-touch on each MIDI channel.

    ## Args

    * `index` (`int`): index on channel rack or mixer.

    * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to `-1`.

    * `useGlobalIndex` (`bool`, optional): whether to use global channel
      indexes when modifying plugins on the channel rack. Defaults to `False`.

    ## Returns

    * `int`: number of parameters.

    Included since API version 8.

    ## API Changes

    * v26: add `useGlobalIndex` flag.
    """
    return 0


@since(8)
def getParamName(
    paramIndex: int,
    index: int,
    slotIndex: int = -1,
    useGlobalIndex: bool = False,
) -> str:
    """
    Returns the name of the parameter at `paramIndex` for the plugin at
    `index`/`slotIndex`.

    ## Args

    * `paramIndex` (`int`): index of parameter.

    * `index` (`int`): index of plugin on channel rack or mixer.

    * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to `-1`.

    * `useGlobalIndex` (`bool`, optional): whether to use global channel
      indexes when modifying plugins on the channel rack. Defaults to `False`.

    ## Returns

    * `str`: name of parameter.

    Included since API version 8.

    ## API Changes

    * v26: add `useGlobalIndex` flag.
    """
    return ""


@since(8)
def getParamValue(
    paramIndex: int,
    index: int,
    slotIndex: int = -1,
    useGlobalIndex: bool = False,
) -> float:
    """
    Returns the value of the parameter at `paramIndex` for the plugin at
    `index`/`slotIndex`.

    ## Args

    * `paramIndex` (`int`): index of parameter.

    * `index` (`int`): index of plugin on channel rack or mixer.

    * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to `-1`.

    * `useGlobalIndex` (`bool`, optional): whether to use global channel
      indexes when modifying plugins on the channel rack. Defaults to `False`.

    ## Returns

    * `float`: parameter value, between `0.0` and `1.0`.

    Included since API version 8.

    ## API Changes

    * v26: add `useGlobalIndex` flag.
    """
    return 0.0


@since(8)
def setParamValue(
    value: float,
    paramIndex: int,
    index: int,
    slotIndex: int = -1,
    pickupMode: int = 0,
    useGlobalIndex: bool = False,
) -> None:
    """
    Sets the value of the parameter at `paramIndex` for the plugin at
    `index`/`slotIndex`.

    ## Args

    * `value` (`float`): new value of parameter (between `0.0` and `1.0`).

    * `paramIndex` (`int`): index of parameter.

    * `index` (`int`): index of plugin on channel rack or mixer.

    * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to `-1`.

    * `pickupMode` (`int`, optional): pickup mode to use:

          * `0`: do not use pickup.
          * `1`: always use pickup.
          * `2`: use pickup if FL Studio is configured to do so.

    * `useGlobalIndex` (`bool`, optional): whether to use global channel
      indexes when modifying plugins on the channel rack. Defaults to `False`.

    Included since API version 8.

    ## API Changes

    * v26: add `useGlobalIndex` flag.
    """


@since(8)
def getParamValueString(
    paramIndex: int,
    index: int,
    slotIndex: int = -1,
    pickupMode: int = midi.PIM_None,
    useGlobalIndex: bool = False,
) -> str:
    """
    Returns a string value of the parameter at `paramIndex` for the plugin at
    `index`/`slotIndex`. This function is only supported by some FL Studio
    plugins.

    ## HELP WANTED

    * What plugins does this support?

    ## Args

    * `paramIndex` (`int`): index of parameter.

    * `index` (`int`): index of plugin on channel rack or mixer.

    * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to `-1`.

    * `useGlobalIndex` (`bool`, optional): whether to use global channel
      indexes when modifying plugins on the channel rack. Defaults to `False`.

    ## Returns

    * `str`: string parameter value.

    Included since API version 8.

    ## API Changes

    * v26: add `useGlobalIndex` flag.
    """
    return ""


@since(12)
def getColor(
    index: int,
    slotIndex: int = -1,
    flag: int = midi.GC_BackgroundColor,
    useGlobalIndex: bool = False,
) -> int:
    """
    Returns various plugin color parameter values for the plugin at
    `index`/`slotIndex`.

    Note that colors can be split into or built from components using the
    functions provided in the module [utils](https://miguelguthridge.github.io/FL-Studio-API-Stubs/utils/).

    * [ColorToRGB()](https://miguelguthridge.github.io/FL-Studio-API-Stubs/utils/#utils.ColorToRGB)

    * [RGBToColor()](https://miguelguthridge.github.io/FL-Studio-API-Stubs/utils/#utils.RGBToColor)

    ## Args

    * `index` (`int`): index of plugin on channel rack or mixer.

    * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to `-1`.

    * `flag` (`int`, optional): color type to return:
          * `GC_BackgroundColor` (`0`, default): The darkest background color
          of the plugin.

          * `GC_Semitone` (`1`): Retrieves semitone color (in FPC, returns
            color of drum pads).

    * `useGlobalIndex` (`bool`, optional): whether to use global channel
      indexes when modifying plugins on the channel rack. Defaults to `False`.

    ## Returns

    * `int`: color (`0x--BBGGRR`).

    Included since API version 12.

    ## API Changes

    * v26: add `useGlobalIndex` flag.
    """
    return 0


@since(13)
def getName(
    index: int,
    slotIndex: int = -1,
    flag: int = midi.FPN_Param,
    paramIndex: int = 0,
    useGlobalIndex: bool = False,
) -> str:
    """
    Returns various names for parts of plugins for the plugin at
    `index`/`slotIndex`.

    ## HELP WANTED

    * Explanation of `flag` values from `3` onwards, excluding `6`.

    * `@overload` decorations of this function that match its optional
      parameter requirements. I couldn't figure it out.

    ## Args

    * `index` (`int`): index of plugin on channel rack or mixer.

    * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to `-1`.

    * `flag` (`int`, optional): name type to return. Names marked with a `*`
      require the `paramIndex` parameter in order to work correctly.
          * `FPN_Param` (`0`, default) `*` : Name of plugin parameter.
              * Eg: `"Expression"`

          * `FPN_ParamValue` (`1`) `*` : Text value of plugin parameter.
              * Eg: `"62%"`

          * `FPN_Semitone` (`2`) `*` : Name of note as defined by plugin.
              * `paramIndex` should be the note number (eg `60` for middle C)

              * If note names aren't defined by the plugin, an empty string is given.

              * Eg: `"Kick"`

          * `FPN_Patch` (`3`): Name of the patch defined by plugin?

          * `FPN_VoiceLevel` (`4`) `*` : Name of per-voice parameter defined by plugin.

          * `FPN_VoiceLevelHint` (`5`) `*` : Hint for per-voice parameter defined by plugin.

          * `FPN_Preset` (`6`) `*` : For plugins that support internal presets, the name of the preset at `paramIndex`.
              * Eg: `"Dystopian lead"`

          * `FPN_OutCtrl` (`7`): For plugins that output controllers, the name of the output controller?

          * `FPN_VoiceColor` (`8`): Name of per-voice color
              * `paramIndex` as MIDI channel?

          * `FPN_VoiceColor` (`9`): For plugins that output voices, the name of output voice
              * `paramIndex` as voice number?

    * `paramIndex` (`int`, optional): index required by requested flag (if
      necessary).

    * `useGlobalIndex` (`bool`, optional): whether to use global channel
      indexes when modifying plugins on the channel rack. Defaults to `False`.

    ## Returns

    * `str`: name of requested parameter.

    Included since API version 13.

    ## API Changes

    * v26: add `useGlobalIndex` flag.
    """
    return ""


@since(19)
def getPadInfo(
    chanIndex: int,
    slotIndex: int = -1,
    paramOption: int = 0,
    paramIndex: int = -1,
    useGlobalIndex: bool = False,
) -> int:
    """
    Returns info about drum pads.

    Currently only supported by FPC.

    ## Args

    * `chanIndex` (`int`): channel of plugin to check.

    * `slotIndex` (`int`, optional): slot of mixer track plugin. Defaults to
      `-1`.

    * `paramOption` (`int`, optional): type of query:
          * `0`: number of pads.

          * `1`: semitone number of pad (use `paramIndex`).

          * `2`: color of pad as 0xBBGGRR (use `paramIndex`).

    * `paramIndex` (`int`, optional): drum pad number (0-indexed).

    * `useGlobalIndex` (`bool`, optional): whether to use global channel
      indexes when modifying plugins on the channel rack. Defaults to `False`.

    ## Returns:
    * `int`: number of drum pads, or

    * `int`: note number of pad, or

    * `int`: color of pad.

    Included since API Version 19.

    ## API Changes

    * v26: add `useGlobalIndex` flag.
    """
    return 0


@since(15)
def getPresetCount(
    index: int,
    slotIndex: int = -1,
    useGlobalIndex: bool = False,
) -> int:
    """
    Returns the number of presets available for the selected plugin.

    ## Args

    * `index` (`int`): index of plugin on channel rack or mixer.

    * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to `-1`.

    * `useGlobalIndex` (`bool`, optional): whether to use global channel
      indexes when modifying plugins on the channel rack. Defaults to `False`.

    Included since API version 15.

    ## API Changes

    * v26: add `useGlobalIndex` flag.
    """
    return 0


@since(10)
def nextPreset(
    index: int,
    slotIndex: int = -1,
    useGlobalIndex: bool = False,
) -> None:
    """
    Navigate to the next preset for plugin at `index`/`slotIndex`.

    ## Args

    * `index` (`int`): index of plugin on channel rack or mixer.

    * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to `-1`.

    * `useGlobalIndex` (`bool`, optional): whether to use global channel
      indexes when modifying plugins on the channel rack. Defaults to `False`.

    Included since API version 10.

    ## API Changes

    * v26: add `useGlobalIndex` flag.
    """


@since(10)
def prevPreset(
    index: int,
    slotIndex: int = -1,
    useGlobalIndex: bool = False,
) -> None:
    """
    Navigate to the previous preset for plugin at `index`/`slotIndex`.

    ## Args

    * `index` (`int`): index of plugin on channel rack or mixer.

    * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to `-1`.

    * `useGlobalIndex` (`bool`, optional): whether to use global channel
      indexes when modifying plugins on the channel rack. Defaults to `False`.

    Included since API version 10.

    ## API Changes

    * v26: add `useGlobalIndex` flag.
    """
