"""
channels > notes

Function definitions for managing notes on channels
"""
from fl_model.decorators import since
from fl_model.channels import checkGlobalIndex, checkGroupIndex


def midiNoteOn(
    indexGlobal: int,
    note: int,
    velocity: int,
    channel: int = -1,
) -> None:
    """
    Set a MIDI Note for the channel at `indexGlobal` (not respecting groups).

    This can be used to create extra notes (eg mapping one note to a chord).

    Note that triggering notes using this function rather than allowing FL
    Studio to process them may result in users' manual note mappings won't be
    respected. Developers should be sure to check
    `channels.getChannelMidiInPort` on all channels to ensure that no channels
    receive MIDI events from this script.

    ## Note

    * Specifying a `channel` doesn't appear to do anything.

    ## Args

    * `indexGlobal` (`int`): channel index (not respecting groups).

    * `note` (`int`): note number (0-127).

    * `velocity` (`int`): note velocity (1-127, 0 is note off).

    * `channel` (`int`, optional): MIDI channel to use. Defaults to -1.

    Included since API version 1.
    """
    checkGlobalIndex(indexGlobal)
    # TODO: Maintain list of note ons for each channel


@since(9)
def quickQuantize(
    index: int,
    startOnly: int = 1,
    useGlobalIndex: bool = False,
) -> None:
    """
    Perform a quick quantize operation on the channel at index

    ## Args

    * `index` (`int`): channel index, respecting groups

    * `startOnly` (`int`, optional): ???. Defaults to `1`.

    * `useGlobalIndex` (`bool`, optional): whether to use the global channel
      index when quantizing notes on the channel.

    Included since API Version 9.

    ## API Changes

    * v33: add `useGlobalIndex` flag.
    """
    checkGroupIndex(index)
