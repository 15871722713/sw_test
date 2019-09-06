# -*- coding: utf-8 -*-
# @Author: JinHua
# @Date:   2019-09-04 13:28:28
# @Last Modified by:   JinHua
# @Last Modified time: 2019-09-06 11:18:11

from config_read import get_config_by_name

ip = get_config_by_name('STC', 'ip')
slotA = get_config_by_name('STC', 'slotA')
slotB = get_config_by_name('STC', 'slotB')
portA = get_config_by_name('STC', 'portA')
portB = get_config_by_name('STC', 'portB')
macA = get_config_by_name('STC', 'macA')
macB = get_config_by_name('STC', 'macB')
vlan = get_config_by_name('STC', 'vlan')
bw = get_config_by_name('STC', 'bw')

stc_path = get_config_by_name('STC', 'path')
path = stc_path + 'Spirenttestcenter.tcl'
cmds = [
    'source "{}"'.format(path),
    'set PortA [stc::create "Port" -under project1 -Location "//{}/{}/{}"]'.format(ip, slotA, portA),
    'set PortB [stc::create "Port" -under project1 -Location "//{}/{}/{}"]'.format(ip, slotB, portB),
    'set port_List "$PortA $PortB"',
    'stc::perform attachPorts -autoConnect true -portList [ stc::get project1 -children-port]',
    'stc::config [stc::get [stc::get $PortA -children-generator] -children]  -SchedulingMode RATE_BASED',
    'stc::config [stc::get [stc::get $PortB -children-generator] -children] -SchedulingMode RATE_BASED',
    'set StreamBlock1 [stc::create "StreamBlock" -under $PortA ]',
    'set StreamBlock1_EthHeader [stc::get $StreamBlock1 -children-ethernet:ethernetii]',
    'stc::config $StreamBlock1_EthHeader -dstMac {} -srcMac {}'.format(macA, macB),
    'set vlanif1 [stc::get $StreamBlock1_EthHeader -children-vlans]',
    'stc::create "vlan" -under $vlanif1 -id {}'.format(vlan),
    'set StreamBlock2 [stc::create "StreamBlock" -under $PortB ]',
    'set StreamBlock2_EthHeader [stc::get $StreamBlock2 -children-ethernet:ethernetii]',
    'stc::config $StreamBlock2_EthHeader -dstMac {} -srcMac {}'.format(macB, macA),
    'set vlanif2 [stc::get $StreamBlock2_EthHeader -children-vlans]',
    'stc::create "vlan" -under $vlanif2 -id {}'.format(vlan),
    'set streamblock1Load [stc::get $StreamBlock1 -affiliationstreamblockloadprofile-Targets]',
    'set streamblock2Load [stc::get $StreamBlock2 -affiliationstreamblockloadprofile-Targets]',
    'stc::config $streamblock1Load -LoadUnit MEGABITS_PER_SECOND -load {}'.format(bw),
    'stc::config $streamblock2Load -LoadUnit MEGABITS_PER_SECOND -load {}'.format(bw),
    'stc::config $StreamBlock1  -FixedFrameLength 512',
    'stc::config $StreamBlock2  -FixedFrameLength 512',
    'set streamblock_List "$StreamBlock1 $StreamBlock2"',
    'stc::subscribe -Parent Project1 -ConfigType StreamBlock -ResultType TxStreamResults',
    'stc::subscribe -Parent Project1 -ConfigType StreamBlock -ResultType RxStreamSummaryResults',
    'stc::apply',
    'stc::perform ResultsClearAll -PortList $port_List -ExecuteSynchronous True',
    'after 5000',
    'stc::perform StreamBlockStart -StreamBlockList $streamblock_List',
    'after 10000',
    'stc::perform StreamBlockStop -StreamBlockList $streamblock_List',
    'after 5000',
    'set format_str "%-15s %-15s %-15s %-15s"',
    'puts [format $format_str Name  TxCount RxCount DropCount]',
    'set streamName [stc::get streamblock1 -Name]',
    'set txStreamResult [stc::get streamblock1 -children-txstreamresults]',
    'set rxStreamResult [stc::get streamblock1 -children-rxstreamsummaryresults]',
    'set txFrameCount [stc::get $txStreamResult -FrameCount]',
    'set rxFrameCount [stc::get $rxStreamResult -SigFrameCount]',
    'set dropCount [stc::get $rxStreamResult -DroppedFrameCount]',
    'puts  [format $format_str $streamName $txFrameCount $rxFrameCount $dropCount]',
    'set streamName [stc::get streamblock2 -Name]',
    'set txStreamResult [stc::get streamblock2 -children-txstreamresults]',
    'set rxStreamResult [stc::get streamblock2 -children-rxstreamsummaryresults]',
    'set txFrameCount [stc::get $txStreamResult -FrameCount]',
    'set rxFrameCount [stc::get $rxStreamResult -SigFrameCount]',
    'set dropCount [stc::get $rxStreamResult -DroppedFrameCount]',
    'puts  [format $format_str $streamName $txFrameCount $rxFrameCount $dropCount]',
    'stc::perform saveasxml -filename {C:/2.xml}'
]
