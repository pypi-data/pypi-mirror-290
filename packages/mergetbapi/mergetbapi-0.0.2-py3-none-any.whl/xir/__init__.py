# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: mergetb/xir/v0.3/core.proto
# plugin: python-betterproto
# This file has been @generated

from dataclasses import dataclass
from typing import (
    Dict,
    List,
)

import betterproto


class Routing(betterproto.Enum):
    ManualRouting = 0
    StaticRouting = 1


class Addressing(betterproto.Enum):
    ManualAddressing = 0
    IPv4Addressing = 1


class Emulation(betterproto.Enum):
    Netem = 0
    Click = 1


class Protocol(betterproto.Enum):
    http = 0
    https = 1
    tcp = 2
    udp = 3


class Isa(betterproto.Enum):
    X86_64 = 0


class MemoryType(betterproto.Enum):
    DDR3 = 0
    DDR4 = 1


class NicModel(betterproto.Enum):
    Intel200 = 0
    Intel300 = 1
    Intel500 = 2
    Intel700 = 3
    Intel800 = 4
    Intel7000 = 50
    Intel8000 = 51
    Intel9000 = 52
    ConnectX4 = 101
    ConnectX5 = 102
    ConnectX6 = 103
    NetXtreme2 = 201
    QCA9000 = 301
    Virtio = 10001
    E1000 = 10002
    E1000E = 10003


class NicKind(betterproto.Enum):
    ETH = 0
    """Ethernet"""

    ENP = 1
    """Ethernet peripheral"""

    ENO = 2
    """Ethernet onboard"""

    ENS = 3
    """Ethernet peripheral hotplog slot"""

    WLP = 4
    """WiFi peripheral"""

    SWP = 5
    """Switch port"""

    IPMI = 6
    """IPMI/BMC"""

    Combo = 7
    """IPMI/BMC + System Ethernet"""


class Layer1(betterproto.Enum):
    Layer1_Undefined = 0
    Base100T = 1
    """100 mbps"""

    Base1000T = 2
    """1 gbps"""

    Base1000X = 3
    Base1000CX = 4
    Base1000SX = 5
    Base1000LX = 6
    Base1000LX10 = 7
    Base1000EX = 8
    Base1000BX10 = 9
    Base1000ZX = 10
    GBase10T = 11
    """10 gbps"""

    GBase10CR = 12
    GBase10SR = 13
    GBase10LR = 14
    GBase10LRM = 15
    GBase10ER = 16
    GBase10ZR = 17
    GBase10LX4 = 18
    GBase10PR = 19
    GBase25CR = 20
    """25 gbps"""

    GBase25SR = 21
    GBase25LR = 22
    GBase25ER = 23
    GBase40CR4 = 24
    """40 gbps"""

    GBase40SR4 = 25
    GBase40LR4 = 26
    GBase40ER4 = 27
    GBase100CR4 = 28
    """100 gbps"""

    GBase100SR4 = 29
    GBase100SR10 = 30
    GBase100LR4 = 31
    GBase100ER4 = 32
    RS232 = 33
    """Console"""

    Uart = 34
    GBase50SR4 = 35
    """50 gbps"""

    GBase50LR4 = 36
    GBase50ER4 = 37
    GBase50CR = 38
    GBase50KR = 39
    GBase50SR = 40
    GBase50LR = 41
    GBase50FR = 42
    GBase50ER = 43
    LAUI_2 = 44
    GAUI50_1 = 45
    GAUI50_2 = 46
    GBase200CR4 = 47
    """200 gbps"""

    GBase200KR4 = 48
    GBase200SR4 = 49
    GBase200DR4 = 50
    GBase200FR4 = 51
    GBase200LR4 = 52
    GBase200ER4 = 53
    GAUI200_4 = 54
    GAUI200_8 = 55
    GBase400SR16 = 56
    """400 gbps"""

    GBase400SR8 = 57
    GBase400SR4_2 = 58
    GBase400DR4 = 59
    GBase400FR8 = 60
    GBase400ER8 = 61
    GBase400ZR = 62
    GAUI400_16 = 63
    GAUI400_8 = 64
    XBee = 65
    ZWave = 66
    Zigbee = 67
    CXP100 = 68
    CXP120 = 69


class ConnectorKind(betterproto.Enum):
    ConnectorKind_Undefined = 0
    RJ45 = 1
    SFP = 2
    QSFP = 3
    SFPP = 4
    QSFPP = 5
    SFP28 = 6
    QSFP28 = 7
    CXP = 8
    LC = 9
    MPO = 10
    SFP56 = 11
    QSFP56 = 12
    QSFPDD = 13


class DiskFormFactor(betterproto.Enum):
    DiskFormFactor_Undefined = 0
    HDD35 = 1
    HDD25 = 2
    SSD35 = 3
    SSD25 = 4
    MSATA = 5
    M2_2216 = 6
    M2_2226 = 7
    M2_2230 = 8
    M2_2238 = 9
    M2_2242 = 10
    M2_2260 = 11
    M2_2280 = 12
    M2_22110 = 13
    U2 = 14
    EMMC = 15
    EUSB = 16
    U3 = 17
    E1S = 18


class DiskInterface(betterproto.Enum):
    DiskInterface_Undefined = 0
    SATA1 = 1
    SATA2 = 2
    SATA3 = 3
    NVMEx2 = 4
    NVMEx4 = 5
    MMC = 6
    SD = 7
    USB = 8
    SAS = 9
    VirtioBlock = 10


class CableKind(betterproto.Enum):
    CableKind_Undefined = 0
    Cat5 = 1
    Cat5e = 2
    Cat6 = 3
    DAC = 4
    DACBreakout = 5
    FiberLC = 6
    FiberMPOTrunk = 7
    FiberMPOBreakout = 8
    AOC = 9
    AOCBreakout = 10
    GenericBreakout = 11
    ACC = 12
    ACCBreakout = 13


class AllocMode(betterproto.Enum):
    AllocMode_Undefined = 0
    NoAlloc = 1
    Net = 2
    NetEmu = 3
    Filesystem = 4
    BlockDevice = 5
    Physical = 6
    Virtual = 7
    Infrapod = 8
    Physim = 9


class Role(betterproto.Enum):
    Role_unknown = 0
    TbNode = 1
    InfraServer = 2
    ConsoleServer = 3
    PowerController = 4
    NetworkEmulator = 5
    XpSwitch = 6
    InfraSwitch = 7
    MgmtSwitch = 8
    Gateway = 9
    Leaf = 10
    Fabric = 11
    Spine = 12
    StorageServer = 13
    InfrapodServer = 14
    EtcdHost = 15
    MinIOHost = 16
    RexHost = 17
    DriverHost = 18
    ManagerHost = 19
    CommanderHost = 20
    SledHost = 21
    RallyHost = 22
    PDU = 23
    EmuSwitch = 24
    Hypervisor = 25
    PhysicsSimulator = 26
    Stem = 27
    BorderGateway = 28
    OpsServer = 29


class LinkRole(betterproto.Enum):
    LinkRole_Unspecified = 0
    InfraLink = 1
    XpLink = 2
    Tor = 3
    EmuLink = 4
    MgmtLink = 5
    GatewayLink = 6
    SimLink = 7
    HarborEndpoint = 8


class DiskRole(betterproto.Enum):
    DiskRole_Unspecified = 0
    System = 1
    MinIO = 2
    Etcd = 3
    Rally = 4
    Mariner = 5


class Operator(betterproto.Enum):
    Op_Undefined = 0
    LT = 1
    LE = 2
    GT = 3
    GE = 4
    EQ = 5
    NE = 6


class LinkKind(betterproto.Enum):
    unspec = 0
    ethernet = 1
    wifi = 2
    wifi_ac = 3
    wifi_ax = 4
    lte_4g = 5
    lte_5g = 6


class BmcKind(betterproto.Enum):
    IPMI = 0
    RedFish = 1
    IPMIRedFish = 2


class RelayBoardKind(betterproto.Enum):
    NCDFusion = 0


class PowerDistributionUnitKind(betterproto.Enum):
    APC = 0


class FirmwareKind(betterproto.Enum):
    Undefined = 0
    UEFI = 1
    BIOS = 2


@dataclass(eq=False, repr=False)
class Facility(betterproto.Message):
    id: str = betterproto.string_field(1)
    fqdn: str = betterproto.string_field(2)
    resources: List["Resource"] = betterproto.message_field(3)
    cables: List["Cable"] = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class Network(betterproto.Message):
    id: str = betterproto.string_field(1)
    nodes: List["Node"] = betterproto.message_field(2)
    links: List["Link"] = betterproto.message_field(3)
    parameters: "ExperimentParameters" = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class ExperimentParameters(betterproto.Message):
    routing: "RoutingConstraint" = betterproto.message_field(1)
    addressing: "AddressingConstraint" = betterproto.message_field(2)
    hypervisors: List[str] = betterproto.string_field(3)
    simulators: List[str] = betterproto.string_field(4)
    emulators: List[str] = betterproto.string_field(5)
    experimentnetresolution: bool = betterproto.bool_field(6)
    emulation: "EmulationConstraint" = betterproto.message_field(7)


@dataclass(eq=False, repr=False)
class Properties(betterproto.Message):
    keyvalues: Dict[str, "PropertiesValues"] = betterproto.map_field(
        1, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )


@dataclass(eq=False, repr=False)
class PropertiesValues(betterproto.Message):
    values: List[str] = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class Node(betterproto.Message):
    id: str = betterproto.string_field(1)
    sockets: List["Socket"] = betterproto.message_field(2)
    proc: "ProcSpec" = betterproto.message_field(3)
    memory: "MemorySpec" = betterproto.message_field(4)
    nic: "NicSpec" = betterproto.message_field(5)
    disks: "DiskSpec" = betterproto.message_field(6)
    metal: "BoolConstraint" = betterproto.message_field(7)
    virt: "BoolConstraint" = betterproto.message_field(8)
    image: "StringConstraint" = betterproto.message_field(9)
    platform: "StringConstraint" = betterproto.message_field(10)
    viz: "Visualization" = betterproto.message_field(11)
    conf: "NodeConfig" = betterproto.message_field(12)
    properties: "Properties" = betterproto.message_field(13)
    """Run time and post-publish properties"""

    host: "StringConstraint" = betterproto.message_field(14)


@dataclass(eq=False, repr=False)
class NodeConfig(betterproto.Message):
    routes: List["RouteConfig"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class RouteConfig(betterproto.Message):
    src: str = betterproto.string_field(1)
    gw: str = betterproto.string_field(2)
    dst: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class Visualization(betterproto.Message):
    color: str = betterproto.string_field(1)
    size: int = betterproto.uint32_field(2)


@dataclass(eq=False, repr=False)
class Ref(betterproto.Message):
    element: str = betterproto.string_field(1)
    index: int = betterproto.uint32_field(2)
    subref: "Subref" = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class Subref(betterproto.Message):
    index: int = betterproto.uint32_field(1)


@dataclass(eq=False, repr=False)
class Socket(betterproto.Message):
    index: int = betterproto.int32_field(1)
    addrs: List[str] = betterproto.string_field(2)
    endpoint: "Ref" = betterproto.message_field(3)
    port: "PortSpec" = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class RouteConf(betterproto.Message):
    src: str = betterproto.string_field(1)
    gw: str = betterproto.string_field(2)
    dst: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class Link(betterproto.Message):
    id: str = betterproto.string_field(1)
    latency: "Uint64Constraint" = betterproto.message_field(2)
    capacity: "Uint64Constraint" = betterproto.message_field(3)
    loss: "FloatConstraint" = betterproto.message_field(4)
    endpoints: List["Endpoint"] = betterproto.message_field(5)
    kind: "LinkKindConstraint" = betterproto.message_field(6)
    layer: "Uint64Constraint" = betterproto.message_field(7)
    properties: "Properties" = betterproto.message_field(8)
    """Run time and post-publish properties"""


@dataclass(eq=False, repr=False)
class Endpoint(betterproto.Message):
    index: int = betterproto.int32_field(1)
    socket: "Ref" = betterproto.message_field(2)
    connector: "ConnectorSpec" = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class Phyo(betterproto.Message):
    id: str = betterproto.string_field(1)
    eqtns: List[str] = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class Variable(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class Bond(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class Coupling(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class Sensor(betterproto.Message):
    id: str = betterproto.string_field(1)
    var: str = betterproto.string_field(2)
    rate: float = betterproto.float_field(3)
    target: str = betterproto.string_field(4)
    tag: int = betterproto.int32_field(5)


@dataclass(eq=False, repr=False)
class Actuator(betterproto.Message):
    id: str = betterproto.string_field(1)
    var: str = betterproto.string_field(2)
    dynamic_limits: "Limits" = betterproto.message_field(3)
    static_limits: "Limits" = betterproto.message_field(4)
    tag: int = betterproto.int32_field(5)


@dataclass(eq=False, repr=False)
class Limits(betterproto.Message):
    lower: float = betterproto.float_field(1)
    upper: float = betterproto.float_field(2)


@dataclass(eq=False, repr=False)
class ProductInfo(betterproto.Message):
    manufacturer: str = betterproto.string_field(1)
    model: str = betterproto.string_field(2)
    sku: str = betterproto.string_field(3)
    integrated: bool = betterproto.bool_field(4)
    cost: float = betterproto.float_field(5)


@dataclass(eq=False, repr=False)
class Resource(betterproto.Message):
    id: str = betterproto.string_field(1)
    facility: str = betterproto.string_field(2)
    procs: List["Proc"] = betterproto.message_field(3)
    memory: List["Dimm"] = betterproto.message_field(4)
    ni_cs: List["Nic"] = betterproto.message_field(5)
    disks: List["Disk"] = betterproto.message_field(6)
    alloc: List["AllocMode"] = betterproto.enum_field(7)
    roles: List["Role"] = betterproto.enum_field(8)
    firmware: "Firmware" = betterproto.message_field(9)
    os: "OsConfig" = betterproto.message_field(10)
    product_info: "ProductInfo" = betterproto.message_field(11)
    tpa: int = betterproto.uint64_field(12)
    ipmi: "Bmc" = betterproto.message_field(13, group="power_control")
    relayboard: "RelayBoard" = betterproto.message_field(14, group="power_control")
    pdu: "PowerDistributionUnit" = betterproto.message_field(15, group="power_control")
    raven: "Raven" = betterproto.message_field(16, group="power_control")
    leaf_config: "LeafConfig" = betterproto.message_field(17)
    infranet_addr: Dict[str, "AddressList"] = betterproto.map_field(
        18, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )


@dataclass(eq=False, repr=False)
class Bmc(betterproto.Message):
    host: str = betterproto.string_field(1)
    kind: "BmcKind" = betterproto.enum_field(2)


@dataclass(eq=False, repr=False)
class RelayBoard(betterproto.Message):
    host: str = betterproto.string_field(1)
    index: int = betterproto.uint32_field(2)
    kind: "RelayBoardKind" = betterproto.enum_field(3)


@dataclass(eq=False, repr=False)
class PowerDistributionUnit(betterproto.Message):
    host: str = betterproto.string_field(1)
    outlets: List[int] = betterproto.uint32_field(2)
    kind: "PowerDistributionUnitKind" = betterproto.enum_field(3)


@dataclass(eq=False, repr=False)
class Raven(betterproto.Message):
    host: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class Firmware(betterproto.Message):
    kind: "FirmwareKind" = betterproto.enum_field(1)


@dataclass(eq=False, repr=False)
class ResourceAllocation(betterproto.Message):
    resource: str = betterproto.string_field(1)
    facility: str = betterproto.string_field(2)
    mzid: str = betterproto.string_field(3)
    node: str = betterproto.string_field(4)
    procs: "ProcAllocation" = betterproto.message_field(5)
    memory: "MemoryAllocation" = betterproto.message_field(6)
    ni_cs: "NiCsAllocation" = betterproto.message_field(7)
    disks: "DisksAllocation" = betterproto.message_field(8)
    model: "Node" = betterproto.message_field(9)
    revision: int = betterproto.int64_field(10)
    virtual: bool = betterproto.bool_field(11)


@dataclass(eq=False, repr=False)
class CableAllocation(betterproto.Message):
    cable: str = betterproto.string_field(1)
    facility: str = betterproto.string_field(2)
    mzid: str = betterproto.string_field(3)
    link: str = betterproto.string_field(4)
    capacity: int = betterproto.uint64_field(5)
    revision: int = betterproto.int64_field(6)


@dataclass(eq=False, repr=False)
class AddressList(betterproto.Message):
    list: List[str] = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class LeafConfig(betterproto.Message):
    service_address_blocks: "AddressList" = betterproto.message_field(1)
    tenant_address_blocks: "AddressList" = betterproto.message_field(2)
    infrapod_address_blocks: Dict[str, "AddressList"] = betterproto.map_field(
        3, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    """interface -> address block"""


@dataclass(eq=False, repr=False)
class OsConfig(betterproto.Message):
    bgp: List["BgpRouterConfig"] = betterproto.message_field(1)
    bridge: List["BridgeConfig"] = betterproto.message_field(2)
    vlan: List["VlanConfig"] = betterproto.message_field(3)
    service_endpoints: Dict[int, "ServiceEndpoint"] = betterproto.map_field(
        4, betterproto.TYPE_UINT32, betterproto.TYPE_MESSAGE
    )
    append: str = betterproto.string_field(5)
    rootdev: str = betterproto.string_field(6)
    default_image: str = betterproto.string_field(7)


@dataclass(eq=False, repr=False)
class ServiceEndpoint(betterproto.Message):
    address: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class VlanConfig(betterproto.Message):
    device: str = betterproto.string_field(1)
    vid: int = betterproto.uint32_field(2)
    addrs: List[str] = betterproto.string_field(3)
    role: "LinkRole" = betterproto.enum_field(4)


@dataclass(eq=False, repr=False)
class InterfaceConfig(betterproto.Message):
    address: str = betterproto.string_field(1)
    interface: str = betterproto.string_field(2)
    role: "LinkRole" = betterproto.enum_field(3)


@dataclass(eq=False, repr=False)
class BgpRouterConfig(betterproto.Message):
    vrf: str = betterproto.string_field(1)
    asn: int = betterproto.uint32_field(2)
    interfaces: List["InterfaceConfig"] = betterproto.message_field(3)
    evpn: "EvpnConfig" = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class EvpnConfig(betterproto.Message):
    tunnel_endpoints: List["InterfaceConfig"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class BridgeConfig(betterproto.Message):
    name: str = betterproto.string_field(1)
    vlan_aware: bool = betterproto.bool_field(2)
    addrs: List[str] = betterproto.string_field(3)
    role: "LinkRole" = betterproto.enum_field(4)


@dataclass(eq=False, repr=False)
class Breakout(betterproto.Message):
    index: int = betterproto.uint32_field(1)
    radix: int = betterproto.uint32_field(2)


@dataclass(eq=False, repr=False)
class PortBond(betterproto.Message):
    name: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class SriovPf(betterproto.Message):
    """SRIOV data"""

    max_v_fs: int = betterproto.uint32_field(1)


@dataclass(eq=False, repr=False)
class SriovVf(betterproto.Message):
    vf_index: int = betterproto.uint32_field(1)


@dataclass(eq=False, repr=False)
class Sriov(betterproto.Message):
    pf: "SriovPf" = betterproto.message_field(2, group="Data")
    vf: "SriovVf" = betterproto.message_field(3, group="Data")
    pf_ni: int = betterproto.uint32_field(4)
    """
    the following two are for quick lookup of PF ports in:
    Resource.NICs[PfNi].Ports[PfPi] -> Port Node.Nic[PfNi][PfPi] -> PortSpec
    ResourceAllocation.NICs.Alloc[PfNi].Alloc[PfPi] -> PortAllocation
    """

    pf_pi: int = betterproto.uint32_field(5)


@dataclass(eq=False, repr=False)
class Port(betterproto.Message):
    parent: str = betterproto.string_field(1)
    index: int = betterproto.uint32_field(2)
    protocols: List["Layer1"] = betterproto.enum_field(3)
    capacity: int = betterproto.uint64_field(4)
    mac: str = betterproto.string_field(5)
    form_factor: "ConnectorKind" = betterproto.enum_field(6)
    connector: "Ref" = betterproto.message_field(7)
    role: "LinkRole" = betterproto.enum_field(8)
    tpa: int = betterproto.uint64_field(9)
    queues: int = betterproto.uint64_field(10)
    breakout: "Breakout" = betterproto.message_field(11)
    bond: "PortBond" = betterproto.message_field(12)
    name: str = betterproto.string_field(13)
    sriov: "Sriov" = betterproto.message_field(14)


@dataclass(eq=False, repr=False)
class BridgeMember(betterproto.Message):
    bridge: str = betterproto.string_field(1)
    vid: int = betterproto.uint32_field(2)


@dataclass(eq=False, repr=False)
class PortAllocation(betterproto.Message):
    name: str = betterproto.string_field(1)
    mac: str = betterproto.string_field(2)
    capacity: int = betterproto.uint64_field(3)
    """
    for VFs: the bandwidth allocated for PFs: the aggregate allocated bandwidth
    (across all allocated vfs)
    """

    vf_name: str = betterproto.string_field(4)
    """
    when describing VM, name can be eth0, eth1, etc. while VfName will be the
    host's actual vf dev
    """

    vf_alloc: bool = betterproto.bool_field(5)
    """for PFs: this port has indirect (VF) allocations"""

    bridge: "BridgeMember" = betterproto.message_field(6)


@dataclass(eq=False, repr=False)
class PortRef(betterproto.Message):
    mac: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class PortSpec(betterproto.Message):
    protocols: List["Layer1"] = betterproto.enum_field(1)
    capacity: "Uint64Constraint" = betterproto.message_field(2)
    form_factor: "ConnectorKindConstraint" = betterproto.message_field(3)
    queues: "Uint64Constraint" = betterproto.message_field(4)
    model: "NicModelConstraint" = betterproto.message_field(5)
    dpdk: "BoolConstraint" = betterproto.message_field(6)
    sriov_vf: "BoolConstraint" = betterproto.message_field(7)


@dataclass(eq=False, repr=False)
class Cable(betterproto.Message):
    id: str = betterproto.string_field(1)
    facility: str = betterproto.string_field(2)
    kind: "CableKind" = betterproto.enum_field(3)
    ends: List["End"] = betterproto.message_field(4)
    product_info: "ProductInfo" = betterproto.message_field(5)


@dataclass(eq=False, repr=False)
class End(betterproto.Message):
    connectors: List["Connector"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class Connector(betterproto.Message):
    parent: str = betterproto.string_field(1)
    index: int = betterproto.uint32_field(2)
    kind: "ConnectorKind" = betterproto.enum_field(3)
    protocols: List["Layer1"] = betterproto.enum_field(4)
    capacity: int = betterproto.uint64_field(5)
    port: "Ref" = betterproto.message_field(6)
    breakout: "Breakout" = betterproto.message_field(7)


@dataclass(eq=False, repr=False)
class ConnectorSpec(betterproto.Message):
    kind: "ConnectorKindConstraint" = betterproto.message_field(1)
    protocols: List["Layer1"] = betterproto.enum_field(2)
    capacity: int = betterproto.uint64_field(3)


@dataclass(eq=False, repr=False)
class Proc(betterproto.Message):
    isa: "Isa" = betterproto.enum_field(1)
    family: str = betterproto.string_field(2)
    base_frequency: int = betterproto.uint64_field(3)
    l2: int = betterproto.uint64_field(4)
    cores: int = betterproto.uint32_field(5)
    threads: int = betterproto.uint32_field(6)
    tdp: int = betterproto.uint32_field(7)
    hyperthreaded: bool = betterproto.bool_field(8)
    product_info: "ProductInfo" = betterproto.message_field(9)
    reserved_cores: int = betterproto.uint32_field(10)


@dataclass(eq=False, repr=False)
class SocketAllocation(betterproto.Message):
    cores: int = betterproto.uint32_field(1)


@dataclass(eq=False, repr=False)
class ProcAllocation(betterproto.Message):
    alloc: Dict[int, "SocketAllocation"] = betterproto.map_field(
        1, betterproto.TYPE_UINT32, betterproto.TYPE_MESSAGE
    )


@dataclass(eq=False, repr=False)
class ProcSpec(betterproto.Message):
    isa: "IsaConstraint" = betterproto.message_field(1)
    family: "StringConstraint" = betterproto.message_field(2)
    base_frequency: "Uint64Constraint" = betterproto.message_field(3)
    l2: "Uint64Constraint" = betterproto.message_field(4)
    cores: "Uint32Constraint" = betterproto.message_field(5)
    threads: "Uint32Constraint" = betterproto.message_field(6)
    tdp: "Uint32Constraint" = betterproto.message_field(7)
    sockets: "Uint32Constraint" = betterproto.message_field(8)
    hyperthreaded: "BoolConstraint" = betterproto.message_field(9)


@dataclass(eq=False, repr=False)
class Dimm(betterproto.Message):
    type: "MemoryType" = betterproto.enum_field(1)
    capacity: int = betterproto.uint64_field(2)
    frequency: int = betterproto.uint64_field(3)
    product_info: "ProductInfo" = betterproto.message_field(4)
    reserved_capacity: int = betterproto.uint64_field(5)


@dataclass(eq=False, repr=False)
class DimmAllocation(betterproto.Message):
    capacity: int = betterproto.uint64_field(1)


@dataclass(eq=False, repr=False)
class MemoryAllocation(betterproto.Message):
    alloc: Dict[int, "DimmAllocation"] = betterproto.map_field(
        1, betterproto.TYPE_UINT32, betterproto.TYPE_MESSAGE
    )


@dataclass(eq=False, repr=False)
class MemorySpec(betterproto.Message):
    type: "MemoryTypeConstraint" = betterproto.message_field(1)
    capacity: "Uint64Constraint" = betterproto.message_field(2)
    frequency: "Uint64Constraint" = betterproto.message_field(3)
    modules: "Uint64Constraint" = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class Nic(betterproto.Message):
    ports: List["Port"] = betterproto.message_field(1)
    starting_index: int = betterproto.uint32_field(2)
    kind: "NicKind" = betterproto.enum_field(3)
    product_info: "ProductInfo" = betterproto.message_field(4)
    dpdk: bool = betterproto.bool_field(5)
    model: "NicModel" = betterproto.enum_field(6)


@dataclass(eq=False, repr=False)
class NicSpec(betterproto.Message):
    ports: List["PortSpec"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class NicAllocation(betterproto.Message):
    alloc: Dict[int, "PortAllocation"] = betterproto.map_field(
        1, betterproto.TYPE_UINT32, betterproto.TYPE_MESSAGE
    )


@dataclass(eq=False, repr=False)
class NiCsAllocation(betterproto.Message):
    alloc: Dict[int, "NicAllocation"] = betterproto.map_field(
        1, betterproto.TYPE_UINT32, betterproto.TYPE_MESSAGE
    )


@dataclass(eq=False, repr=False)
class Disk(betterproto.Message):
    capacity: int = betterproto.uint64_field(1)
    form_factor: "DiskFormFactor" = betterproto.enum_field(2)
    disk_interface: "DiskInterface" = betterproto.enum_field(3)
    product_info: "ProductInfo" = betterproto.message_field(4)
    roles: List["DiskRole"] = betterproto.enum_field(5)
    nvme_controller_index: int = betterproto.uint32_field(6)


@dataclass(eq=False, repr=False)
class DiskAllocation(betterproto.Message):
    capacity: int = betterproto.uint64_field(1)


@dataclass(eq=False, repr=False)
class DisksAllocation(betterproto.Message):
    alloc: Dict[int, "DiskAllocation"] = betterproto.map_field(
        1, betterproto.TYPE_UINT32, betterproto.TYPE_MESSAGE
    )


@dataclass(eq=False, repr=False)
class DiskSpec(betterproto.Message):
    capacity: "Uint64Constraint" = betterproto.message_field(1)
    form_factor: "DiskFormFactorConstraint" = betterproto.message_field(2)
    disk_interface: "DiskInterfaceConstraint" = betterproto.message_field(3)
    disks: "Uint64Constraint" = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class BoolConstraint(betterproto.Message):
    op: "Operator" = betterproto.enum_field(1)
    value: bool = betterproto.bool_field(2)


@dataclass(eq=False, repr=False)
class StringConstraint(betterproto.Message):
    op: "Operator" = betterproto.enum_field(1)
    value: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class Uint64Constraint(betterproto.Message):
    op: "Operator" = betterproto.enum_field(1)
    value: int = betterproto.uint64_field(2)


@dataclass(eq=False, repr=False)
class LinkKindConstraint(betterproto.Message):
    op: "Operator" = betterproto.enum_field(1)
    value: "LinkKind" = betterproto.enum_field(2)


@dataclass(eq=False, repr=False)
class Uint32Constraint(betterproto.Message):
    op: "Operator" = betterproto.enum_field(1)
    value: int = betterproto.uint32_field(2)


@dataclass(eq=False, repr=False)
class IsaConstraint(betterproto.Message):
    op: "Operator" = betterproto.enum_field(1)
    value: "Isa" = betterproto.enum_field(2)


@dataclass(eq=False, repr=False)
class MemoryTypeConstraint(betterproto.Message):
    op: "Operator" = betterproto.enum_field(1)
    value: "MemoryType" = betterproto.enum_field(2)


@dataclass(eq=False, repr=False)
class NicModelConstraint(betterproto.Message):
    op: "Operator" = betterproto.enum_field(1)
    value: "NicModel" = betterproto.enum_field(2)


@dataclass(eq=False, repr=False)
class DiskFormFactorConstraint(betterproto.Message):
    op: "Operator" = betterproto.enum_field(1)
    value: "DiskFormFactor" = betterproto.enum_field(2)


@dataclass(eq=False, repr=False)
class DiskInterfaceConstraint(betterproto.Message):
    op: "Operator" = betterproto.enum_field(1)
    value: "DiskInterface" = betterproto.enum_field(2)


@dataclass(eq=False, repr=False)
class ConnectorKindConstraint(betterproto.Message):
    op: "Operator" = betterproto.enum_field(1)
    value: "ConnectorKind" = betterproto.enum_field(2)


@dataclass(eq=False, repr=False)
class FloatConstraint(betterproto.Message):
    op: "Operator" = betterproto.enum_field(1)
    value: float = betterproto.float_field(2)


@dataclass(eq=False, repr=False)
class RoutingConstraint(betterproto.Message):
    op: "Operator" = betterproto.enum_field(1)
    value: "Routing" = betterproto.enum_field(2)


@dataclass(eq=False, repr=False)
class AddressingConstraint(betterproto.Message):
    op: "Operator" = betterproto.enum_field(1)
    value: "Addressing" = betterproto.enum_field(2)


@dataclass(eq=False, repr=False)
class EmulationConstraint(betterproto.Message):
    op: "Operator" = betterproto.enum_field(1)
    value: "Emulation" = betterproto.enum_field(2)
