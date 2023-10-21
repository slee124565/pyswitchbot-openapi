from typing import List
from switchbot.domain import model


def _make_fake_dev_states() -> List[model.SwitchBotStatus]:
    state_data_list = [
        {
            "deviceId": "6055F92FCFD2",
            "deviceType": "Plug Mini (US)",
            "hubDeviceId": "6055F92FCFD2",
            "power": "off",
            "version": "V1.4-1.4",
            "voltage": 114.7,
            "weight": 0.0,
            "electricityOfDay": 3,
            "electricCurrent": 0.0
        },
        {
            "deviceId": "6055F930FF22",
            "deviceType": "Plug Mini (US)",
            "hubDeviceId": "6055F930FF22",
            "power": "off",
            "version": "V1.4-1.4",
            "voltage": 114.7,
            "weight": 0.0,
            "electricityOfDay": 122,
            "electricCurrent": 0.0
        }
    ]
    return [model.SwitchBotStatus.load(data) for data in state_data_list]


def _make_initial_user_devices() -> model.SwitchBotUserRepo:
    _a = model.SwitchBotDevice(
        device_id='6055F92FCFD2',
        device_name='小風扇開關',
        device_type='Plug Mini (US)',
        enable_cloud_service=True,
        hub_device_id=''
    )
    _b = model.SwitchBotDevice(
        device_id='6055F930FF22',
        device_name='風扇開關',
        device_type='Plug Mini (US)',
        enable_cloud_service=True,
        hub_device_id=''
    )
    _a.state = model.SwitchBotStatus.load({
        "deviceId": "6055F92FCFD2",
        "deviceType": "Plug Mini (US)",
        "hubDeviceId": "6055F92FCFD2",
        "power": "off",
        "version": "V1.4-1.4",
        "voltage": 114.7,
        "weight": 0.0,
        "electricityOfDay": 3,
        "electricCurrent": 0.0
    })
    _b.state = model.SwitchBotStatus.load({
        "deviceId": "6055F930FF22",
        "deviceType": "Plug Mini (US)",
        "hubDeviceId": "6055F930FF22",
        "power": "off",
        "version": "V1.4-1.4",
        "voltage": 114.7,
        "weight": 0.0,
        "electricityOfDay": 122,
        "electricCurrent": 0.0
    })

    return model.SwitchBotUserRepo(
        user_id='user_id',
        secret='secret',
        token='token',
        devices=[_a, _b],
        states=[],
        scenes=[],
        webhooks=[]
    )


def test_request_sync_with_new_device_added():
    """設備新增"""
    devices = [
        model.SwitchBotDevice(
            device_id='6055F92FCFD2',
            device_name='小風扇開關',
            device_type='Plug Mini (US)',
            enable_cloud_service=True,
            hub_device_id=''
        ),
        model.SwitchBotDevice(
            device_id='6055F930FF22',
            device_name='風扇開關',
            device_type='Plug Mini (US)',
            enable_cloud_service=True,
            hub_device_id=''
        ),
    ]
    user = model.SwitchBotUserRepo(
        user_id='user_id',
        secret='secret',
        token='token',
        devices=[],
        states=[],
        scenes=[],
        webhooks=[]
    )

    user.request_sync(devices=devices)

    assert len(user.devices) == 2
    assert set([dev.device_id for dev in user.devices]) == {'6055F92FCFD2', '6055F930FF22'}


def test_request_sync_with_device_name_changed():
    """設備名稱變更"""
    sync_devices = [
        model.SwitchBotDevice(
            device_id='6055F92FCFD2',
            device_name='小風扇開關',
            device_type='Plug Mini (US)',
            enable_cloud_service=True,
            hub_device_id=''
        ),
        model.SwitchBotDevice(
            device_id='6055F930FF22',
            device_name='床頭燈',
            device_type='Plug Mini (US)',
            enable_cloud_service=True,
            hub_device_id=''
        )
    ]
    user = _make_initial_user_devices()

    user.request_sync(devices=sync_devices)

    for dev in user.devices:
        if dev.device_id == '6055F92FCFD2':
            assert dev.device_name == '小風扇開關'
        elif dev.device_id == '6055F930FF22':
            assert dev.device_name == '床頭燈'
        else:
            assert False
    assert len(user.devices) == 2


def test_request_sync_with_device_removed():
    """設備移除"""
    sync_devices = [
        model.SwitchBotDevice(
            device_id='6055F92FCFD2',
            device_name='小風扇開關',
            device_type='Plug Mini (US)',
            enable_cloud_service=True,
            hub_device_id=''
        )
    ]
    user = _make_initial_user_devices()

    user.request_sync(devices=sync_devices)

    assert len(user.devices) == 1
    device = user.devices[0]
    assert device.device_id == '6055F92FCFD2'
    assert device.device_name == '小風扇開關'
    assert device.device_type == 'Plug Mini (US)'


def test_request_sync_device_with_no_changed():
    """設備維持不變"""
    sync_devices = [
        model.SwitchBotDevice(
            device_id='6055F92FCFD2',
            device_name='小風扇開關',
            device_type='Plug Mini (US)',
            enable_cloud_service=True,
            hub_device_id=''
        ),
        model.SwitchBotDevice(
            device_id='6055F930FF22',
            device_name='床頭燈',
            device_type='Plug Mini (US)',
            enable_cloud_service=True,
            hub_device_id=''
        )
    ]
    user = _make_initial_user_devices()

    user.request_sync(devices=sync_devices)

    assert len(user.devices) == 2
    assert set([dev.device_id for dev in user.devices]) == {'6055F92FCFD2', '6055F930FF22'}


def test_user_disconnect_from_service():
    """用戶終止設備連線整合控制"""
    user = _make_initial_user_devices()

    user.disconnect()

    assert len(user.devices) == 0


def test_report_state():
    """更新用戶設備狀態"""
    user = _make_initial_user_devices()
    dev_powers = []

    for state in [dev.state for dev in user.devices]:
        state.power = 'on' if state.power == 'off' else 'off'
        dev_powers.append((state.device_id, state.power))  # (dev_id, power)
        user.report_state(state=state)

    for dev_id in ['6055F92FCFD2', '6055F930FF22']:
        _state = next((dev.state for dev in user.devices if dev.device_id == dev_id))
        _power = next((power for _id, power in dev_powers if _id == _state.device_id))
        assert _state.power == _power


def test_query_devices():
    """查詢用戶設備狀態"""
    user = _make_initial_user_devices()

    target_dev_list = [dev.device_id for dev in user.devices]
    state_list = user.query(dev_id_list=target_dev_list)

    assert len(state_list) == len(target_dev_list)
    for state in state_list:
        assert isinstance(state, model.SwitchBotStatus)

# def test_device_exec_one_cmd_on_one_device():
#     raise NotImplementedError
#
#
# def test_device_exec_one_cmd_on_multi_device():
#     raise NotImplementedError
#
#
# def test_device_exec_diff_cmd_on_diff_device():
#     raise NotImplementedError
