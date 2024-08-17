from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/port-channel-interfaces.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_port_channel_interfaces = resolve('port_channel_interfaces')
    l_0_encapsulation_dot1q_interfaces = resolve('encapsulation_dot1q_interfaces')
    l_0_flexencap_interfaces = resolve('flexencap_interfaces')
    l_0_namespace = resolve('namespace')
    l_0_port_channel_interface_pvlan = resolve('port_channel_interface_pvlan')
    l_0_port_channel_interface_vlan_xlate = resolve('port_channel_interface_vlan_xlate')
    l_0_evpn_es_po_interfaces = resolve('evpn_es_po_interfaces')
    l_0_evpn_dfe_po_interfaces = resolve('evpn_dfe_po_interfaces')
    l_0_evpn_mpls_po_interfaces = resolve('evpn_mpls_po_interfaces')
    l_0_link_tracking_interfaces = resolve('link_tracking_interfaces')
    l_0_port_channel_interface_ipv4 = resolve('port_channel_interface_ipv4')
    l_0_ip_nat_interfaces = resolve('ip_nat_interfaces')
    l_0_port_channel_interface_ipv6 = resolve('port_channel_interface_ipv6')
    l_0_port_channel_interfaces_isis = resolve('port_channel_interfaces_isis')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_3 = environment.filters['length']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'length' found.")
    try:
        t_4 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    try:
        t_5 = environment.tests['defined']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No test named 'defined' found.")
    pass
    if t_4((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces)):
        pass
        yield '\n### Port-Channel Interfaces\n\n#### Port-Channel Interfaces Summary\n\n##### L2\n\n| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | LACP Fallback Timeout | LACP Fallback Mode | MLAG ID | EVPN ESI |\n| --------- | ----------- | ---- | ----- | ----------- | ------------| --------------------- | ------------------ | ------- | -------- |\n'
        for l_1_port_channel_interface in t_2((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            l_1_description = resolve('description')
            l_1_mode = resolve('mode')
            l_1_vlans = resolve('vlans')
            l_1_native_vlan = resolve('native_vlan')
            l_1_l2 = resolve('l2')
            l_1_lacp_fallback_timeout = resolve('lacp_fallback_timeout')
            l_1_lacp_fallback_mode = resolve('lacp_fallback_mode')
            l_1_mlag = resolve('mlag')
            l_1_esi = resolve('esi')
            _loop_vars = {}
            pass
            if t_4(environment.getattr(l_1_port_channel_interface, 'type'), 'switched'):
                pass
                l_1_description = t_1(environment.getattr(l_1_port_channel_interface, 'description'), '-')
                _loop_vars['description'] = l_1_description
                l_1_mode = t_1(environment.getattr(l_1_port_channel_interface, 'mode'), 'access')
                _loop_vars['mode'] = l_1_mode
                l_1_vlans = t_1(environment.getattr(l_1_port_channel_interface, 'vlans'), '-')
                _loop_vars['vlans'] = l_1_vlans
                if t_4(environment.getattr(l_1_port_channel_interface, 'native_vlan_tag'), True):
                    pass
                    l_1_native_vlan = 'tag'
                    _loop_vars['native_vlan'] = l_1_native_vlan
                else:
                    pass
                    l_1_native_vlan = t_1(environment.getattr(l_1_port_channel_interface, 'native_vlan'), '-')
                    _loop_vars['native_vlan'] = l_1_native_vlan
                if t_5(environment.getattr(l_1_port_channel_interface, 'trunk_groups')):
                    pass
                    l_1_l2 = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), _loop_vars=_loop_vars)
                    _loop_vars['l2'] = l_1_l2
                    if not isinstance(l_1_l2, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_1_l2['trunk_groups'] = []
                    for l_2_trunk_group in t_2(environment.getattr(l_1_port_channel_interface, 'trunk_groups')):
                        _loop_vars = {}
                        pass
                        context.call(environment.getattr(environment.getattr((undefined(name='l2') if l_1_l2 is missing else l_1_l2), 'trunk_groups'), 'append'), l_2_trunk_group, _loop_vars=_loop_vars)
                    l_2_trunk_group = missing
                else:
                    pass
                    l_1_l2 = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), _loop_vars=_loop_vars)
                    _loop_vars['l2'] = l_1_l2
                    if not isinstance(l_1_l2, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_1_l2['trunk_groups'] = '-'
                l_1_lacp_fallback_timeout = t_1(environment.getattr(l_1_port_channel_interface, 'lacp_fallback_timeout'), '-')
                _loop_vars['lacp_fallback_timeout'] = l_1_lacp_fallback_timeout
                l_1_lacp_fallback_mode = t_1(environment.getattr(l_1_port_channel_interface, 'lacp_fallback_mode'), '-')
                _loop_vars['lacp_fallback_mode'] = l_1_lacp_fallback_mode
                l_1_mlag = t_1(environment.getattr(l_1_port_channel_interface, 'mlag'), '-')
                _loop_vars['mlag'] = l_1_mlag
                l_1_esi = t_1(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'identifier'), '-')
                _loop_vars['esi'] = l_1_esi
                yield '| '
                yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                yield ' | '
                yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                yield ' | '
                yield str((undefined(name='mode') if l_1_mode is missing else l_1_mode))
                yield ' | '
                yield str((undefined(name='vlans') if l_1_vlans is missing else l_1_vlans))
                yield ' | '
                yield str((undefined(name='native_vlan') if l_1_native_vlan is missing else l_1_native_vlan))
                yield ' | '
                yield str(environment.getattr((undefined(name='l2') if l_1_l2 is missing else l_1_l2), 'trunk_groups'))
                yield ' | '
                yield str((undefined(name='lacp_fallback_timeout') if l_1_lacp_fallback_timeout is missing else l_1_lacp_fallback_timeout))
                yield ' | '
                yield str((undefined(name='lacp_fallback_mode') if l_1_lacp_fallback_mode is missing else l_1_lacp_fallback_mode))
                yield ' | '
                yield str((undefined(name='mlag') if l_1_mlag is missing else l_1_mlag))
                yield ' | '
                yield str((undefined(name='esi') if l_1_esi is missing else l_1_esi))
                yield ' |\n'
        l_1_port_channel_interface = l_1_description = l_1_mode = l_1_vlans = l_1_native_vlan = l_1_l2 = l_1_lacp_fallback_timeout = l_1_lacp_fallback_mode = l_1_mlag = l_1_esi = missing
        l_0_encapsulation_dot1q_interfaces = []
        context.vars['encapsulation_dot1q_interfaces'] = l_0_encapsulation_dot1q_interfaces
        context.exported_vars.add('encapsulation_dot1q_interfaces')
        l_0_flexencap_interfaces = []
        context.vars['flexencap_interfaces'] = l_0_flexencap_interfaces
        context.exported_vars.add('flexencap_interfaces')
        for l_1_port_channel_interface in (undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces):
            _loop_vars = {}
            pass
            if (t_1(environment.getattr(l_1_port_channel_interface, 'type')) in ['l3dot1q', 'l2dot1q']):
                pass
                if t_4(environment.getattr(l_1_port_channel_interface, 'encapsulation_dot1q_vlan')):
                    pass
                    context.call(environment.getattr((undefined(name='encapsulation_dot1q_interfaces') if l_0_encapsulation_dot1q_interfaces is missing else l_0_encapsulation_dot1q_interfaces), 'append'), l_1_port_channel_interface, _loop_vars=_loop_vars)
                elif t_4(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan')):
                    pass
                    context.call(environment.getattr((undefined(name='flexencap_interfaces') if l_0_flexencap_interfaces is missing else l_0_flexencap_interfaces), 'append'), l_1_port_channel_interface, _loop_vars=_loop_vars)
        l_1_port_channel_interface = missing
        if (t_3((undefined(name='encapsulation_dot1q_interfaces') if l_0_encapsulation_dot1q_interfaces is missing else l_0_encapsulation_dot1q_interfaces)) > 0):
            pass
            yield '\n##### Encapsulation Dot1q\n\n| Interface | Description | Vlan ID | Dot1q VLAN Tag |\n| --------- | ----------- | ------- | -------------- |\n'
            for l_1_port_channel_interface in t_2((undefined(name='encapsulation_dot1q_interfaces') if l_0_encapsulation_dot1q_interfaces is missing else l_0_encapsulation_dot1q_interfaces), 'name'):
                l_1_description = l_1_vlan_id = l_1_encapsulation_dot1q_vlan = missing
                _loop_vars = {}
                pass
                l_1_description = t_1(environment.getattr(l_1_port_channel_interface, 'description'), '-')
                _loop_vars['description'] = l_1_description
                l_1_vlan_id = t_1(environment.getattr(l_1_port_channel_interface, 'vlan_id'), '-')
                _loop_vars['vlan_id'] = l_1_vlan_id
                l_1_encapsulation_dot1q_vlan = t_1(environment.getattr(l_1_port_channel_interface, 'encapsulation_dot1q_vlan'), '-')
                _loop_vars['encapsulation_dot1q_vlan'] = l_1_encapsulation_dot1q_vlan
                yield '| '
                yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                yield ' | '
                yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                yield ' | '
                yield str((undefined(name='vlan_id') if l_1_vlan_id is missing else l_1_vlan_id))
                yield ' | '
                yield str((undefined(name='encapsulation_dot1q_vlan') if l_1_encapsulation_dot1q_vlan is missing else l_1_encapsulation_dot1q_vlan))
                yield ' |\n'
            l_1_port_channel_interface = l_1_description = l_1_vlan_id = l_1_encapsulation_dot1q_vlan = missing
        if (t_3((undefined(name='flexencap_interfaces') if l_0_flexencap_interfaces is missing else l_0_flexencap_interfaces)) > 0):
            pass
            yield '\n##### Flexible Encapsulation Interfaces\n\n| Interface | Description | Vlan ID | Client Unmatched | Client Dot1q VLAN | Client Dot1q Outer Tag | Client Dot1q Inner Tag | Network Retain Client Encapsulation | Network Dot1q VLAN | Network Dot1q Outer Tag | Network Dot1q Inner Tag |\n| --------- | ----------- | ------- | -----------------| ----------------- | ---------------------- | ---------------------- | ----------------------------------- | ------------------ | ----------------------- | ----------------------- |\n'
            for l_1_port_channel_interface in t_2((undefined(name='flexencap_interfaces') if l_0_flexencap_interfaces is missing else l_0_flexencap_interfaces), 'name'):
                l_1_description = l_1_vlan_id = l_1_client_unmatched = l_1_client_dot1q_vlan = l_1_client_dot1q_outer = l_1_client_dot1q_inner = l_1_network_client = l_1_network_dot1q_vlan = l_1_network_dot1q_outer = l_1_network_dot1q_inner = missing
                _loop_vars = {}
                pass
                l_1_description = t_1(environment.getattr(l_1_port_channel_interface, 'description'), '-')
                _loop_vars['description'] = l_1_description
                l_1_vlan_id = t_1(environment.getattr(l_1_port_channel_interface, 'vlan_id'), '-')
                _loop_vars['vlan_id'] = l_1_vlan_id
                l_1_client_unmatched = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'unmatched'), False)
                _loop_vars['client_unmatched'] = l_1_client_unmatched
                l_1_client_dot1q_vlan = t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'vlan'), '-')
                _loop_vars['client_dot1q_vlan'] = l_1_client_dot1q_vlan
                l_1_client_dot1q_outer = t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'outer'), '-')
                _loop_vars['client_dot1q_outer'] = l_1_client_dot1q_outer
                l_1_client_dot1q_inner = t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'inner'), '-')
                _loop_vars['client_dot1q_inner'] = l_1_client_dot1q_inner
                l_1_network_client = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'client'), False)
                _loop_vars['network_client'] = l_1_network_client
                l_1_network_dot1q_vlan = t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'vlan'), '-')
                _loop_vars['network_dot1q_vlan'] = l_1_network_dot1q_vlan
                l_1_network_dot1q_outer = t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'outer'), '-')
                _loop_vars['network_dot1q_outer'] = l_1_network_dot1q_outer
                l_1_network_dot1q_inner = t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_port_channel_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'inner'), '-')
                _loop_vars['network_dot1q_inner'] = l_1_network_dot1q_inner
                yield '| '
                yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                yield ' | '
                yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                yield ' | '
                yield str((undefined(name='vlan_id') if l_1_vlan_id is missing else l_1_vlan_id))
                yield ' | '
                yield str((undefined(name='client_unmatched') if l_1_client_unmatched is missing else l_1_client_unmatched))
                yield ' | '
                yield str((undefined(name='client_dot1q_vlan') if l_1_client_dot1q_vlan is missing else l_1_client_dot1q_vlan))
                yield ' | '
                yield str((undefined(name='client_dot1q_outer') if l_1_client_dot1q_outer is missing else l_1_client_dot1q_outer))
                yield ' | '
                yield str((undefined(name='client_dot1q_inner') if l_1_client_dot1q_inner is missing else l_1_client_dot1q_inner))
                yield ' | '
                yield str((undefined(name='network_client') if l_1_network_client is missing else l_1_network_client))
                yield ' | '
                yield str((undefined(name='network_dot1q_vlan') if l_1_network_dot1q_vlan is missing else l_1_network_dot1q_vlan))
                yield ' | '
                yield str((undefined(name='network_dot1q_outer') if l_1_network_dot1q_outer is missing else l_1_network_dot1q_outer))
                yield ' | '
                yield str((undefined(name='network_dot1q_inner') if l_1_network_dot1q_inner is missing else l_1_network_dot1q_inner))
                yield ' |\n'
            l_1_port_channel_interface = l_1_description = l_1_vlan_id = l_1_client_unmatched = l_1_client_dot1q_vlan = l_1_client_dot1q_outer = l_1_client_dot1q_inner = l_1_network_client = l_1_network_dot1q_vlan = l_1_network_dot1q_outer = l_1_network_dot1q_inner = missing
        l_0_port_channel_interface_pvlan = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['port_channel_interface_pvlan'] = l_0_port_channel_interface_pvlan
        context.exported_vars.add('port_channel_interface_pvlan')
        if not isinstance(l_0_port_channel_interface_pvlan, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_port_channel_interface_pvlan['configured'] = False
        for l_1_port_channel_interface in t_2((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if (t_4(environment.getattr(l_1_port_channel_interface, 'pvlan_mapping')) or t_4(environment.getattr(l_1_port_channel_interface, 'trunk_private_vlan_secondary'))):
                pass
                if not isinstance(l_0_port_channel_interface_pvlan, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_port_channel_interface_pvlan['configured'] = True
                break
        l_1_port_channel_interface = missing
        if environment.getattr((undefined(name='port_channel_interface_pvlan') if l_0_port_channel_interface_pvlan is missing else l_0_port_channel_interface_pvlan), 'configured'):
            pass
            yield '\n##### Private VLAN\n\n| Interface | PVLAN Mapping | Secondary Trunk |\n| --------- | ------------- | ----------------|\n'
            for l_1_port_channel_interface in t_2((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
                l_1_row_pvlan_mapping = resolve('row_pvlan_mapping')
                l_1_row_trunk_private_vlan_secondary = resolve('row_trunk_private_vlan_secondary')
                _loop_vars = {}
                pass
                if (t_4(environment.getattr(l_1_port_channel_interface, 'pvlan_mapping')) or t_4(environment.getattr(l_1_port_channel_interface, 'trunk_private_vlan_secondary'))):
                    pass
                    l_1_row_pvlan_mapping = t_1(environment.getattr(l_1_port_channel_interface, 'pvlan_mapping'), '-')
                    _loop_vars['row_pvlan_mapping'] = l_1_row_pvlan_mapping
                    l_1_row_trunk_private_vlan_secondary = t_1(environment.getattr(l_1_port_channel_interface, 'trunk_private_vlan_secondary'), '-')
                    _loop_vars['row_trunk_private_vlan_secondary'] = l_1_row_trunk_private_vlan_secondary
                    yield '| '
                    yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='row_pvlan_mapping') if l_1_row_pvlan_mapping is missing else l_1_row_pvlan_mapping))
                    yield ' | '
                    yield str((undefined(name='row_trunk_private_vlan_secondary') if l_1_row_trunk_private_vlan_secondary is missing else l_1_row_trunk_private_vlan_secondary))
                    yield ' |\n'
            l_1_port_channel_interface = l_1_row_pvlan_mapping = l_1_row_trunk_private_vlan_secondary = missing
        l_0_port_channel_interface_vlan_xlate = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['port_channel_interface_vlan_xlate'] = l_0_port_channel_interface_vlan_xlate
        context.exported_vars.add('port_channel_interface_vlan_xlate')
        if not isinstance(l_0_port_channel_interface_vlan_xlate, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_port_channel_interface_vlan_xlate['configured'] = False
        for l_1_port_channel_interface in t_2((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_4(environment.getattr(l_1_port_channel_interface, 'vlan_translations')):
                pass
                if not isinstance(l_0_port_channel_interface_vlan_xlate, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_port_channel_interface_vlan_xlate['configured'] = True
                break
        l_1_port_channel_interface = missing
        if environment.getattr((undefined(name='port_channel_interface_vlan_xlate') if l_0_port_channel_interface_vlan_xlate is missing else l_0_port_channel_interface_vlan_xlate), 'configured'):
            pass
            yield '\n##### VLAN Translations\n\n| Interface | From VLAN ID(s) | To VLAN ID | Direction |\n| --------- | --------------- | -----------| --------- |\n'
            for l_1_port_channel_interface in t_2((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
                _loop_vars = {}
                pass
                if t_4(environment.getattr(l_1_port_channel_interface, 'vlan_translations')):
                    pass
                    for l_2_vlan_translation in t_2(environment.getattr(l_1_port_channel_interface, 'vlan_translations')):
                        l_2_row_direction = resolve('row_direction')
                        _loop_vars = {}
                        pass
                        if (t_4(environment.getattr(l_2_vlan_translation, 'from')) and t_4(environment.getattr(l_2_vlan_translation, 'to'))):
                            pass
                            l_2_row_direction = t_1(environment.getattr(l_2_vlan_translation, 'direction'), 'both')
                            _loop_vars['row_direction'] = l_2_row_direction
                            yield '| '
                            yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                            yield ' | '
                            yield str(environment.getattr(l_2_vlan_translation, 'from'))
                            yield ' | '
                            yield str(environment.getattr(l_2_vlan_translation, 'to'))
                            yield ' | '
                            yield str((undefined(name='row_direction') if l_2_row_direction is missing else l_2_row_direction))
                            yield ' |\n'
                    l_2_vlan_translation = l_2_row_direction = missing
            l_1_port_channel_interface = missing
        l_0_evpn_es_po_interfaces = []
        context.vars['evpn_es_po_interfaces'] = l_0_evpn_es_po_interfaces
        context.exported_vars.add('evpn_es_po_interfaces')
        l_0_evpn_dfe_po_interfaces = []
        context.vars['evpn_dfe_po_interfaces'] = l_0_evpn_dfe_po_interfaces
        context.exported_vars.add('evpn_dfe_po_interfaces')
        l_0_evpn_mpls_po_interfaces = []
        context.vars['evpn_mpls_po_interfaces'] = l_0_evpn_mpls_po_interfaces
        context.exported_vars.add('evpn_mpls_po_interfaces')
        l_0_link_tracking_interfaces = []
        context.vars['link_tracking_interfaces'] = l_0_link_tracking_interfaces
        context.exported_vars.add('link_tracking_interfaces')
        for l_1_port_channel_interface in t_2((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if t_4(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment')):
                pass
                context.call(environment.getattr((undefined(name='evpn_es_po_interfaces') if l_0_evpn_es_po_interfaces is missing else l_0_evpn_es_po_interfaces), 'append'), l_1_port_channel_interface, _loop_vars=_loop_vars)
                if t_4(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election')):
                    pass
                    context.call(environment.getattr((undefined(name='evpn_dfe_po_interfaces') if l_0_evpn_dfe_po_interfaces is missing else l_0_evpn_dfe_po_interfaces), 'append'), l_1_port_channel_interface, _loop_vars=_loop_vars)
                if t_4(environment.getattr(environment.getattr(l_1_port_channel_interface, 'evpn_ethernet_segment'), 'mpls')):
                    pass
                    context.call(environment.getattr((undefined(name='evpn_mpls_po_interfaces') if l_0_evpn_mpls_po_interfaces is missing else l_0_evpn_mpls_po_interfaces), 'append'), l_1_port_channel_interface, _loop_vars=_loop_vars)
            if t_4(environment.getattr(l_1_port_channel_interface, 'link_tracking_groups')):
                pass
                context.call(environment.getattr((undefined(name='link_tracking_interfaces') if l_0_link_tracking_interfaces is missing else l_0_link_tracking_interfaces), 'append'), l_1_port_channel_interface, _loop_vars=_loop_vars)
        l_1_port_channel_interface = missing
        if (t_3((undefined(name='evpn_es_po_interfaces') if l_0_evpn_es_po_interfaces is missing else l_0_evpn_es_po_interfaces)) > 0):
            pass
            yield '\n##### EVPN Multihoming\n\n####### EVPN Multihoming Summary\n\n| Interface | Ethernet Segment Identifier | Multihoming Redundancy Mode | Route Target |\n| --------- | --------------------------- | --------------------------- | ------------ |\n'
            for l_1_evpn_es_po_interface in t_2((undefined(name='evpn_es_po_interfaces') if l_0_evpn_es_po_interfaces is missing else l_0_evpn_es_po_interfaces), 'name'):
                l_1_esi = l_1_redundancy = l_1_rt = missing
                _loop_vars = {}
                pass
                l_1_esi = t_1(environment.getattr(environment.getattr(l_1_evpn_es_po_interface, 'evpn_ethernet_segment'), 'identifier'), environment.getattr(l_1_evpn_es_po_interface, 'esi'), '-')
                _loop_vars['esi'] = l_1_esi
                l_1_redundancy = t_1(environment.getattr(environment.getattr(l_1_evpn_es_po_interface, 'evpn_ethernet_segment'), 'redundancy'), 'all-active')
                _loop_vars['redundancy'] = l_1_redundancy
                l_1_rt = t_1(environment.getattr(environment.getattr(l_1_evpn_es_po_interface, 'evpn_ethernet_segment'), 'route_target'), '-')
                _loop_vars['rt'] = l_1_rt
                yield '| '
                yield str(environment.getattr(l_1_evpn_es_po_interface, 'name'))
                yield ' | '
                yield str((undefined(name='esi') if l_1_esi is missing else l_1_esi))
                yield ' | '
                yield str((undefined(name='redundancy') if l_1_redundancy is missing else l_1_redundancy))
                yield ' | '
                yield str((undefined(name='rt') if l_1_rt is missing else l_1_rt))
                yield ' |\n'
            l_1_evpn_es_po_interface = l_1_esi = l_1_redundancy = l_1_rt = missing
            if (t_3((undefined(name='evpn_dfe_po_interfaces') if l_0_evpn_dfe_po_interfaces is missing else l_0_evpn_dfe_po_interfaces)) > 0):
                pass
                yield '\n####### Designated Forwarder Election Summary\n\n| Interface | Algorithm | Preference Value | Dont Preempt | Hold time | Subsequent Hold Time | Candidate Reachability Required |\n| --------- | --------- | ---------------- | ------------ | --------- | -------------------- | ------------------------------- |\n'
                for l_1_evpn_dfe_po_interface in t_2((undefined(name='evpn_dfe_po_interfaces') if l_0_evpn_dfe_po_interfaces is missing else l_0_evpn_dfe_po_interfaces), 'name'):
                    l_1_df_po_settings = l_1_algorithm = l_1_pref_value = l_1_dont_preempt = l_1_hold_time = l_1_subsequent_hold_time = l_1_candidate_reachability = missing
                    _loop_vars = {}
                    pass
                    l_1_df_po_settings = environment.getattr(environment.getattr(l_1_evpn_dfe_po_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election')
                    _loop_vars['df_po_settings'] = l_1_df_po_settings
                    l_1_algorithm = t_1(environment.getattr((undefined(name='df_po_settings') if l_1_df_po_settings is missing else l_1_df_po_settings), 'algorithm'), 'modulus')
                    _loop_vars['algorithm'] = l_1_algorithm
                    l_1_pref_value = t_1(environment.getattr((undefined(name='df_po_settings') if l_1_df_po_settings is missing else l_1_df_po_settings), 'preference_value'), '-')
                    _loop_vars['pref_value'] = l_1_pref_value
                    l_1_dont_preempt = t_1(environment.getattr((undefined(name='df_po_settings') if l_1_df_po_settings is missing else l_1_df_po_settings), 'dont_preempt'), False)
                    _loop_vars['dont_preempt'] = l_1_dont_preempt
                    l_1_hold_time = t_1(environment.getattr((undefined(name='df_po_settings') if l_1_df_po_settings is missing else l_1_df_po_settings), 'hold_time'), '-')
                    _loop_vars['hold_time'] = l_1_hold_time
                    l_1_subsequent_hold_time = t_1(environment.getattr((undefined(name='df_po_settings') if l_1_df_po_settings is missing else l_1_df_po_settings), 'subsequent_hold_time'), '-')
                    _loop_vars['subsequent_hold_time'] = l_1_subsequent_hold_time
                    l_1_candidate_reachability = t_1(environment.getattr((undefined(name='df_po_settings') if l_1_df_po_settings is missing else l_1_df_po_settings), 'candidate_reachability_required'), False)
                    _loop_vars['candidate_reachability'] = l_1_candidate_reachability
                    yield '| '
                    yield str(environment.getattr(l_1_evpn_dfe_po_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='algorithm') if l_1_algorithm is missing else l_1_algorithm))
                    yield ' | '
                    yield str((undefined(name='pref_value') if l_1_pref_value is missing else l_1_pref_value))
                    yield ' | '
                    yield str((undefined(name='dont_preempt') if l_1_dont_preempt is missing else l_1_dont_preempt))
                    yield ' | '
                    yield str((undefined(name='hold_time') if l_1_hold_time is missing else l_1_hold_time))
                    yield ' | '
                    yield str((undefined(name='subsequent_hold_time') if l_1_subsequent_hold_time is missing else l_1_subsequent_hold_time))
                    yield ' | '
                    yield str((undefined(name='candidate_reachability') if l_1_candidate_reachability is missing else l_1_candidate_reachability))
                    yield ' |\n'
                l_1_evpn_dfe_po_interface = l_1_df_po_settings = l_1_algorithm = l_1_pref_value = l_1_dont_preempt = l_1_hold_time = l_1_subsequent_hold_time = l_1_candidate_reachability = missing
            if (t_3((undefined(name='evpn_mpls_po_interfaces') if l_0_evpn_mpls_po_interfaces is missing else l_0_evpn_mpls_po_interfaces)) > 0):
                pass
                yield '\n####### EVPN-MPLS summary\n\n| Interface | Shared Index | Tunnel Flood Filter Time |\n| --------- | ------------ | ------------------------ |\n'
                for l_1_evpn_mpls_po_interface in t_2((undefined(name='evpn_mpls_po_interfaces') if l_0_evpn_mpls_po_interfaces is missing else l_0_evpn_mpls_po_interfaces)):
                    l_1_shared_index = l_1_tff_time = missing
                    _loop_vars = {}
                    pass
                    l_1_shared_index = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_evpn_mpls_po_interface, 'evpn_ethernet_segment'), 'mpls'), 'shared_index'), '-')
                    _loop_vars['shared_index'] = l_1_shared_index
                    l_1_tff_time = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_evpn_mpls_po_interface, 'evpn_ethernet_segment'), 'mpls'), 'tunnel_flood_filter_time'), '-')
                    _loop_vars['tff_time'] = l_1_tff_time
                    yield '| '
                    yield str(environment.getattr(l_1_evpn_mpls_po_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='shared_index') if l_1_shared_index is missing else l_1_shared_index))
                    yield ' | '
                    yield str((undefined(name='tff_time') if l_1_tff_time is missing else l_1_tff_time))
                    yield ' |\n'
                l_1_evpn_mpls_po_interface = l_1_shared_index = l_1_tff_time = missing
        if (t_3((undefined(name='link_tracking_interfaces') if l_0_link_tracking_interfaces is missing else l_0_link_tracking_interfaces)) > 0):
            pass
            yield '\n##### Link Tracking Groups\n\n| Interface | Group Name | Direction |\n| --------- | ---------- | --------- |\n'
            for l_1_link_tracking_interface in t_2((undefined(name='link_tracking_interfaces') if l_0_link_tracking_interfaces is missing else l_0_link_tracking_interfaces), 'name'):
                _loop_vars = {}
                pass
                for l_2_link_tracking_group in t_2(environment.getattr(l_1_link_tracking_interface, 'link_tracking_groups'), 'name'):
                    _loop_vars = {}
                    pass
                    if (t_4(environment.getattr(l_2_link_tracking_group, 'name')) and t_4(environment.getattr(l_2_link_tracking_group, 'direction'))):
                        pass
                        yield '| '
                        yield str(environment.getattr(l_1_link_tracking_interface, 'name'))
                        yield ' | '
                        yield str(environment.getattr(l_2_link_tracking_group, 'name'))
                        yield ' | '
                        yield str(environment.getattr(l_2_link_tracking_group, 'direction'))
                        yield ' |\n'
                l_2_link_tracking_group = missing
            l_1_link_tracking_interface = missing
        l_0_port_channel_interface_ipv4 = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['port_channel_interface_ipv4'] = l_0_port_channel_interface_ipv4
        context.exported_vars.add('port_channel_interface_ipv4')
        if not isinstance(l_0_port_channel_interface_ipv4, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_port_channel_interface_ipv4['configured'] = False
        for l_1_port_channel_interface in t_2((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if ((t_5(environment.getattr(l_1_port_channel_interface, 'type')) and (environment.getattr(l_1_port_channel_interface, 'type') in ['routed', 'l3dot1q'])) and t_5(environment.getattr(l_1_port_channel_interface, 'ip_address'))):
                pass
                if not isinstance(l_0_port_channel_interface_ipv4, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_port_channel_interface_ipv4['configured'] = True
        l_1_port_channel_interface = missing
        if environment.getattr((undefined(name='port_channel_interface_ipv4') if l_0_port_channel_interface_ipv4 is missing else l_0_port_channel_interface_ipv4), 'configured'):
            pass
            yield '\n##### IPv4\n\n| Interface | Description | MLAG ID | IP Address | VRF | MTU | Shutdown | ACL In | ACL Out |\n| --------- | ----------- | ------- | ---------- | --- | --- | -------- | ------ | ------- |\n'
            for l_1_port_channel_interface in t_2((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
                l_1_description = resolve('description')
                l_1_mlag = resolve('mlag')
                l_1_ip_address = resolve('ip_address')
                l_1_vrf = resolve('vrf')
                l_1_mtu = resolve('mtu')
                l_1_shutdown = resolve('shutdown')
                l_1_acl_in = resolve('acl_in')
                l_1_acl_out = resolve('acl_out')
                _loop_vars = {}
                pass
                if ((t_5(environment.getattr(l_1_port_channel_interface, 'type')) and (environment.getattr(l_1_port_channel_interface, 'type') in ['routed', 'l3dot1q'])) and t_4(environment.getattr(l_1_port_channel_interface, 'ip_address'))):
                    pass
                    l_1_description = t_1(environment.getattr(l_1_port_channel_interface, 'description'), '-')
                    _loop_vars['description'] = l_1_description
                    l_1_mlag = t_1(environment.getattr(l_1_port_channel_interface, 'mlag'), '-')
                    _loop_vars['mlag'] = l_1_mlag
                    l_1_ip_address = t_1(environment.getattr(l_1_port_channel_interface, 'ip_address'), '-')
                    _loop_vars['ip_address'] = l_1_ip_address
                    l_1_vrf = t_1(environment.getattr(l_1_port_channel_interface, 'vrf'), 'default')
                    _loop_vars['vrf'] = l_1_vrf
                    l_1_mtu = t_1(environment.getattr(l_1_port_channel_interface, 'mtu'), '-')
                    _loop_vars['mtu'] = l_1_mtu
                    l_1_shutdown = t_1(environment.getattr(l_1_port_channel_interface, 'shutdown'), '-')
                    _loop_vars['shutdown'] = l_1_shutdown
                    l_1_acl_in = t_1(environment.getattr(l_1_port_channel_interface, 'access_group_in'), '-')
                    _loop_vars['acl_in'] = l_1_acl_in
                    l_1_acl_out = t_1(environment.getattr(l_1_port_channel_interface, 'access_group_out'), '-')
                    _loop_vars['acl_out'] = l_1_acl_out
                    yield '| '
                    yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                    yield ' | '
                    yield str((undefined(name='mlag') if l_1_mlag is missing else l_1_mlag))
                    yield ' | '
                    yield str((undefined(name='ip_address') if l_1_ip_address is missing else l_1_ip_address))
                    yield ' | '
                    yield str((undefined(name='vrf') if l_1_vrf is missing else l_1_vrf))
                    yield ' | '
                    yield str((undefined(name='mtu') if l_1_mtu is missing else l_1_mtu))
                    yield ' | '
                    yield str((undefined(name='shutdown') if l_1_shutdown is missing else l_1_shutdown))
                    yield ' | '
                    yield str((undefined(name='acl_in') if l_1_acl_in is missing else l_1_acl_in))
                    yield ' | '
                    yield str((undefined(name='acl_out') if l_1_acl_out is missing else l_1_acl_out))
                    yield ' |\n'
            l_1_port_channel_interface = l_1_description = l_1_mlag = l_1_ip_address = l_1_vrf = l_1_mtu = l_1_shutdown = l_1_acl_in = l_1_acl_out = missing
        l_0_ip_nat_interfaces = (undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces)
        context.vars['ip_nat_interfaces'] = l_0_ip_nat_interfaces
        context.exported_vars.add('ip_nat_interfaces')
        template = environment.get_template('documentation/interfaces-ip-nat.j2', 'documentation/port-channel-interfaces.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {'encapsulation_dot1q_interfaces': l_0_encapsulation_dot1q_interfaces, 'evpn_dfe_po_interfaces': l_0_evpn_dfe_po_interfaces, 'evpn_es_po_interfaces': l_0_evpn_es_po_interfaces, 'evpn_mpls_po_interfaces': l_0_evpn_mpls_po_interfaces, 'flexencap_interfaces': l_0_flexencap_interfaces, 'ip_nat_interfaces': l_0_ip_nat_interfaces, 'link_tracking_interfaces': l_0_link_tracking_interfaces, 'port_channel_interface_ipv4': l_0_port_channel_interface_ipv4, 'port_channel_interface_ipv6': l_0_port_channel_interface_ipv6, 'port_channel_interface_pvlan': l_0_port_channel_interface_pvlan, 'port_channel_interface_vlan_xlate': l_0_port_channel_interface_vlan_xlate, 'port_channel_interfaces_isis': l_0_port_channel_interfaces_isis})):
            yield event
        l_0_port_channel_interface_ipv6 = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['port_channel_interface_ipv6'] = l_0_port_channel_interface_ipv6
        context.exported_vars.add('port_channel_interface_ipv6')
        if not isinstance(l_0_port_channel_interface_ipv6, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_port_channel_interface_ipv6['configured'] = False
        for l_1_port_channel_interface in t_2((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if ((t_5(environment.getattr(l_1_port_channel_interface, 'type')) and (environment.getattr(l_1_port_channel_interface, 'type') in ['routed', 'l3dot1q'])) and t_5(environment.getattr(l_1_port_channel_interface, 'ipv6_address'))):
                pass
                if not isinstance(l_0_port_channel_interface_ipv6, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_0_port_channel_interface_ipv6['configured'] = True
        l_1_port_channel_interface = missing
        if environment.getattr((undefined(name='port_channel_interface_ipv6') if l_0_port_channel_interface_ipv6 is missing else l_0_port_channel_interface_ipv6), 'configured'):
            pass
            yield '\n##### IPv6\n\n| Interface | Description | MLAG ID | IPv6 Address | VRF | MTU | Shutdown | ND RA Disabled | Managed Config Flag | IPv6 ACL In | IPv6 ACL Out |\n| --------- | ----------- | ------- | -------------| --- | --- | -------- | -------------- | ------------------- | ----------- | ------------ |\n'
            for l_1_port_channel_interface in t_2((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
                l_1_description = resolve('description')
                l_1_mlag = resolve('mlag')
                l_1_ipv6_address = resolve('ipv6_address')
                l_1_vrf = resolve('vrf')
                l_1_mtu = resolve('mtu')
                l_1_shutdown = resolve('shutdown')
                l_1_ipv6_nd_ra_disabled = resolve('ipv6_nd_ra_disabled')
                l_1_ipv6_nd_managed_config_flag = resolve('ipv6_nd_managed_config_flag')
                l_1_ipv6_acl_in = resolve('ipv6_acl_in')
                l_1_ipv6_acl_out = resolve('ipv6_acl_out')
                _loop_vars = {}
                pass
                if ((t_5(environment.getattr(l_1_port_channel_interface, 'type')) and (environment.getattr(l_1_port_channel_interface, 'type') in ['routed', 'l3dot1q'])) and t_4(environment.getattr(l_1_port_channel_interface, 'ipv6_address'))):
                    pass
                    l_1_description = t_1(environment.getattr(l_1_port_channel_interface, 'description'), '-')
                    _loop_vars['description'] = l_1_description
                    l_1_mlag = t_1(environment.getattr(l_1_port_channel_interface, 'mlag'), '-')
                    _loop_vars['mlag'] = l_1_mlag
                    l_1_ipv6_address = t_1(environment.getattr(l_1_port_channel_interface, 'ipv6_address'), '-')
                    _loop_vars['ipv6_address'] = l_1_ipv6_address
                    l_1_vrf = t_1(environment.getattr(l_1_port_channel_interface, 'vrf'), 'default')
                    _loop_vars['vrf'] = l_1_vrf
                    l_1_mtu = t_1(environment.getattr(l_1_port_channel_interface, 'mtu'), '-')
                    _loop_vars['mtu'] = l_1_mtu
                    l_1_shutdown = t_1(environment.getattr(l_1_port_channel_interface, 'shutdown'), '-')
                    _loop_vars['shutdown'] = l_1_shutdown
                    l_1_ipv6_nd_ra_disabled = t_1(environment.getattr(l_1_port_channel_interface, 'ipv6_nd_ra_disabled'), '-')
                    _loop_vars['ipv6_nd_ra_disabled'] = l_1_ipv6_nd_ra_disabled
                    if t_4(environment.getattr(l_1_port_channel_interface, 'ipv6_nd_managed_config_flag')):
                        pass
                        l_1_ipv6_nd_managed_config_flag = environment.getattr(l_1_port_channel_interface, 'ipv6_nd_managed_config_flag')
                        _loop_vars['ipv6_nd_managed_config_flag'] = l_1_ipv6_nd_managed_config_flag
                    else:
                        pass
                        l_1_ipv6_nd_managed_config_flag = '-'
                        _loop_vars['ipv6_nd_managed_config_flag'] = l_1_ipv6_nd_managed_config_flag
                    l_1_ipv6_acl_in = t_1(environment.getattr(l_1_port_channel_interface, 'ipv6_access_group_in'), '-')
                    _loop_vars['ipv6_acl_in'] = l_1_ipv6_acl_in
                    l_1_ipv6_acl_out = t_1(environment.getattr(l_1_port_channel_interface, 'ipv6_access_group_out'), '-')
                    _loop_vars['ipv6_acl_out'] = l_1_ipv6_acl_out
                    yield '| '
                    yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                    yield ' | '
                    yield str((undefined(name='description') if l_1_description is missing else l_1_description))
                    yield ' | '
                    yield str((undefined(name='mlag') if l_1_mlag is missing else l_1_mlag))
                    yield ' | '
                    yield str((undefined(name='ipv6_address') if l_1_ipv6_address is missing else l_1_ipv6_address))
                    yield ' | '
                    yield str((undefined(name='vrf') if l_1_vrf is missing else l_1_vrf))
                    yield ' | '
                    yield str((undefined(name='mtu') if l_1_mtu is missing else l_1_mtu))
                    yield ' | '
                    yield str((undefined(name='shutdown') if l_1_shutdown is missing else l_1_shutdown))
                    yield ' | '
                    yield str((undefined(name='ipv6_nd_ra_disabled') if l_1_ipv6_nd_ra_disabled is missing else l_1_ipv6_nd_ra_disabled))
                    yield ' | '
                    yield str((undefined(name='ipv6_nd_managed_config_flag') if l_1_ipv6_nd_managed_config_flag is missing else l_1_ipv6_nd_managed_config_flag))
                    yield ' | '
                    yield str((undefined(name='ipv6_acl_in') if l_1_ipv6_acl_in is missing else l_1_ipv6_acl_in))
                    yield ' | '
                    yield str((undefined(name='ipv6_acl_out') if l_1_ipv6_acl_out is missing else l_1_ipv6_acl_out))
                    yield ' |\n'
            l_1_port_channel_interface = l_1_description = l_1_mlag = l_1_ipv6_address = l_1_vrf = l_1_mtu = l_1_shutdown = l_1_ipv6_nd_ra_disabled = l_1_ipv6_nd_managed_config_flag = l_1_ipv6_acl_in = l_1_ipv6_acl_out = missing
        l_0_port_channel_interfaces_isis = []
        context.vars['port_channel_interfaces_isis'] = l_0_port_channel_interfaces_isis
        context.exported_vars.add('port_channel_interfaces_isis')
        for l_1_port_channel_interface in t_2((undefined(name='port_channel_interfaces') if l_0_port_channel_interfaces is missing else l_0_port_channel_interfaces), 'name'):
            _loop_vars = {}
            pass
            if (((((((t_4(environment.getattr(l_1_port_channel_interface, 'isis_enable')) or t_4(environment.getattr(l_1_port_channel_interface, 'isis_bfd'))) or t_4(environment.getattr(l_1_port_channel_interface, 'isis_metric'))) or t_4(environment.getattr(l_1_port_channel_interface, 'isis_circuit_type'))) or t_4(environment.getattr(l_1_port_channel_interface, 'isis_network_point_to_point'))) or t_4(environment.getattr(l_1_port_channel_interface, 'isis_passive'))) or t_4(environment.getattr(l_1_port_channel_interface, 'isis_hello_padding'))) or t_4(environment.getattr(l_1_port_channel_interface, 'isis_authentication_mode'))):
                pass
                context.call(environment.getattr((undefined(name='port_channel_interfaces_isis') if l_0_port_channel_interfaces_isis is missing else l_0_port_channel_interfaces_isis), 'append'), l_1_port_channel_interface, _loop_vars=_loop_vars)
        l_1_port_channel_interface = missing
        if (t_3((undefined(name='port_channel_interfaces_isis') if l_0_port_channel_interfaces_isis is missing else l_0_port_channel_interfaces_isis)) > 0):
            pass
            yield '\n##### ISIS\n\n| Interface | ISIS Instance | ISIS BFD | ISIS Metric | Mode | ISIS Circuit Type | Hello Padding | Authentication Mode |\n| --------- | ------------- | -------- | ----------- | ---- | ----------------- | ------------- | ------------------- |\n'
            for l_1_port_channel_interface in t_2((undefined(name='port_channel_interfaces_isis') if l_0_port_channel_interfaces_isis is missing else l_0_port_channel_interfaces_isis), 'name'):
                l_1_isis_instance = l_1_isis_bfd = l_1_isis_metric = l_1_isis_circuit_type = l_1_isis_hello_padding = l_1_isis_authentication_mode = l_1_mode = missing
                _loop_vars = {}
                pass
                l_1_isis_instance = t_1(environment.getattr(l_1_port_channel_interface, 'isis_enable'), '-')
                _loop_vars['isis_instance'] = l_1_isis_instance
                l_1_isis_bfd = t_1(environment.getattr(l_1_port_channel_interface, 'isis_bfd'), '-')
                _loop_vars['isis_bfd'] = l_1_isis_bfd
                l_1_isis_metric = t_1(environment.getattr(l_1_port_channel_interface, 'isis_metric'), '-')
                _loop_vars['isis_metric'] = l_1_isis_metric
                l_1_isis_circuit_type = t_1(environment.getattr(l_1_port_channel_interface, 'isis_circuit_type'), '-')
                _loop_vars['isis_circuit_type'] = l_1_isis_circuit_type
                l_1_isis_hello_padding = t_1(environment.getattr(l_1_port_channel_interface, 'isis_hello_padding'), '-')
                _loop_vars['isis_hello_padding'] = l_1_isis_hello_padding
                l_1_isis_authentication_mode = t_1(environment.getattr(l_1_port_channel_interface, 'isis_authentication_mode'), '-')
                _loop_vars['isis_authentication_mode'] = l_1_isis_authentication_mode
                if t_4(environment.getattr(l_1_port_channel_interface, 'isis_network_point_to_point'), True):
                    pass
                    l_1_mode = 'point-to-point'
                    _loop_vars['mode'] = l_1_mode
                elif t_4(environment.getattr(l_1_port_channel_interface, 'isis_passive'), True):
                    pass
                    l_1_mode = 'passive'
                    _loop_vars['mode'] = l_1_mode
                else:
                    pass
                    l_1_mode = '-'
                    _loop_vars['mode'] = l_1_mode
                yield '| '
                yield str(environment.getattr(l_1_port_channel_interface, 'name'))
                yield ' | '
                yield str((undefined(name='isis_instance') if l_1_isis_instance is missing else l_1_isis_instance))
                yield ' | '
                yield str((undefined(name='isis_bfd') if l_1_isis_bfd is missing else l_1_isis_bfd))
                yield ' | '
                yield str((undefined(name='isis_metric') if l_1_isis_metric is missing else l_1_isis_metric))
                yield ' | '
                yield str((undefined(name='mode') if l_1_mode is missing else l_1_mode))
                yield ' | '
                yield str((undefined(name='isis_circuit_type') if l_1_isis_circuit_type is missing else l_1_isis_circuit_type))
                yield ' | '
                yield str((undefined(name='isis_hello_padding') if l_1_isis_hello_padding is missing else l_1_isis_hello_padding))
                yield ' | '
                yield str((undefined(name='isis_authentication_mode') if l_1_isis_authentication_mode is missing else l_1_isis_authentication_mode))
                yield ' |\n'
            l_1_port_channel_interface = l_1_isis_instance = l_1_isis_bfd = l_1_isis_metric = l_1_isis_circuit_type = l_1_isis_hello_padding = l_1_isis_authentication_mode = l_1_mode = missing
        yield '\n#### Port-Channel Interfaces Device Configuration\n\n```eos\n'
        template = environment.get_template('eos/port-channel-interfaces.j2', 'documentation/port-channel-interfaces.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {'encapsulation_dot1q_interfaces': l_0_encapsulation_dot1q_interfaces, 'evpn_dfe_po_interfaces': l_0_evpn_dfe_po_interfaces, 'evpn_es_po_interfaces': l_0_evpn_es_po_interfaces, 'evpn_mpls_po_interfaces': l_0_evpn_mpls_po_interfaces, 'flexencap_interfaces': l_0_flexencap_interfaces, 'ip_nat_interfaces': l_0_ip_nat_interfaces, 'link_tracking_interfaces': l_0_link_tracking_interfaces, 'port_channel_interface_ipv4': l_0_port_channel_interface_ipv4, 'port_channel_interface_ipv6': l_0_port_channel_interface_ipv6, 'port_channel_interface_pvlan': l_0_port_channel_interface_pvlan, 'port_channel_interface_vlan_xlate': l_0_port_channel_interface_vlan_xlate, 'port_channel_interfaces_isis': l_0_port_channel_interfaces_isis})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '7=55&17=58&18=70&19=72&20=74&21=76&22=78&23=80&25=84&27=86&28=88&29=90&30=93&31=96&34=100&35=102&37=105&38=107&39=109&40=111&41=114&45=135&46=138&47=141&48=144&49=146&50=148&51=149&52=151&56=153&62=156&63=160&64=162&65=164&66=167&69=176&75=179&76=183&77=185&78=187&79=189&80=191&81=193&82=195&83=197&84=199&85=201&86=204&90=227&91=230&92=233&93=236&95=238&96=241&99=243&105=246&106=251&108=253&109=255&110=258&115=265&116=268&117=271&118=274&119=276&120=279&123=281&129=284&130=287&131=289&132=293&133=295&134=298&141=308&142=311&143=314&144=317&145=320&146=323&147=325&148=326&149=328&151=329&152=331&155=332&156=334&160=336&168=339&169=343&170=345&171=347&172=350&174=359&180=362&181=366&182=368&183=370&184=372&185=374&186=376&187=378&188=381&191=396&197=399&198=403&199=405&200=408&205=415&211=418&212=421&213=424&214=427&220=435&221=438&222=441&223=444&224=446&227=450&233=453&234=464&235=466&236=468&237=470&238=472&239=474&240=476&241=478&242=480&243=483&248=502&249=505&251=508&252=511&253=514&254=517&255=519&258=523&264=526&265=539&266=541&267=543&268=545&269=547&270=549&271=551&272=553&273=555&274=557&276=561&278=563&279=565&280=568&285=591&286=594&287=597&295=599&298=601&304=604&305=608&306=610&307=612&308=614&309=616&310=618&311=620&312=622&313=624&314=626&316=630&318=633&325=651'