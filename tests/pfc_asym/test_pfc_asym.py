from tests.ptf_runner import ptf_runner
import pytest

pytestmark = [
    pytest.mark.topology('t0')
]

def test_pfc_asym_off_tx_pfc(ptfhost, setup, pfc_storm_runner):
    """
    @summary: Asymmetric PFC is disabled. Verify that DUT generates PFC frames only on lossless priorities when
                asymmetric PFC is disabled
    @param ptfhost: Fixture which can run ansible modules on the PTF host
    @param setup: Fixture which performs setup/tardown steps needed for test case preparation
    """
    pfc_storm_runner.non_server_port = True
    pfc_storm_runner.run()

    ptf_runner(ptfhost,
                "saitests",
                "pfc_asym.PfcAsymOffOnTxTest",
                platform_dir="ptftests",
                params=setup["ptf_test_params"],
                log_file="/tmp/pfc_asym.PfcAsymOffOnTxTest.log")


def test_pfc_asym_off_rx_pause_frames(ptfhost, setup, pfc_storm_runner):
    """
    @summary: Asymmetric PFC is disabled. Verify that while receiving PFC frames DUT drops packets only for lossless
                priorities (RX and Tx queue buffers are full)
    @param ptfhost: Fixture which can run ansible modules on the PTF host
    @param setup: Fixture which performs setup/tardown steps needed for test case preparation
    @param pfc_storm_runner: Fixture which start/stop PFC generator on Fanout switch
    """

    # Due to limitation on Tofino 1 we do not differentiate the RX PFC with the priority it holds but stop
    # the whole traffic. That's why this test case is skipped for BFN platfrom. But it should be working
    # on Tofino2 with some driver code modification.
    if setup["ptf_test_params"]["asic_type"] == "barefoot":
        pytest.skip("Not supported for {} asic".format(setup["ptf_test_params"]["asic_type"]))

    pfc_storm_runner.server_ports = True
    pfc_storm_runner.run()

    ptf_runner(ptfhost,
                "saitests",
                "pfc_asym.PfcAsymOffRxTest",
                platform_dir="ptftests",
                params=setup["ptf_test_params"],
                log_file="/tmp/pfc_asym.PfcAsymOffRxTest.log")


def test_pfc_asym_on_tx_pfc(ptfhost, setup, enable_pfc_asym, pfc_storm_runner):
    """
    @summary: Asymmetric PFC is enabled. Verify that DUT generates PFC frames only on lossless priorities when
                asymmetric PFC is enabled
    @param ptfhost: Fixture which can run ansible modules on the PTF host
    @param setup: Fixture which performs setup/tardown steps needed for test case preparation
    @param enable_pfc_asym: Fixture which enable/disable asymmetric PFC on all server interfaces
    """
    pfc_storm_runner.non_server_port = True
    pfc_storm_runner.run()

    ptf_runner(ptfhost,
                "saitests",
                "pfc_asym.PfcAsymOffOnTxTest",
                platform_dir="ptftests",
                params=setup["ptf_test_params"],
                log_file="/tmp/pfc_asym.PfcAsymOffOnTxTest.log")


def test_pfc_asym_on_handle_pfc_all_prio(ptfhost, setup, enable_pfc_asym, pfc_storm_runner):
    """
    @summary: Asymmetric PFC is enabled. Verify that while receiving PFC frames DUT handle PFC frames on all
                priorities when asymetric mode is enabled
    @param ptfhost: Fixture which can run ansible modules on the PTF host
    @param setup: Fixture which performs setup/tardown steps needed for test case preparation
    @param pfc_storm_runner: Fixture which start/stop PFC generator on Fanout switch
    @param enable_pfc_asym: Fixture which enable/disable asymmetric PFC on all server interfaces
    """
    pfc_storm_runner.server_ports = True
    pfc_storm_runner.run()

    ptf_runner(ptfhost,
                "saitests",
                "pfc_asym.PfcAsymOnRxTest",
                platform_dir="ptftests",
                params=setup["ptf_test_params"],
                log_file="/tmp/pfc_asym.PfcAsymOnRxTest.log")
