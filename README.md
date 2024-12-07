python3 -u dynamicinclution.py dynamically
python3 -u dynamicinclution.py  query_name = 'dynamically'

this command get the statistics of usm this usm_build_statistics.py file runs and it takes the quary name as the input 

("BAZEL_IMS_7_8","IMS_7_0_MR","IMS_7_2_MR","IMS_7_4_1_MAIN","IMS_7_6_CDFMC_MAIN","IMS_7_6_CDFMC_RC","IMS_7_6_CDFMC_RC_DROP6","IMS_7_6_MAIN","IMS_7_7_0","IMS_7_7_CDFMC_MAIN","IMS_7_7_MAIN","IMS_7_8_MAIN","liverpool/FXOS_2_10_1","main","oval/FXOS_2_13_0","richmond/FXOS_2_16_MAIN","stratford/FXOS_2_17_MAIN","stratford/fxos_bazel","stratford/ztna_p1","temple/FXOS_2_18_MAIN","ztna_p1")





("BAZEL_IMS_7_8", "IMS_7_0_MR", "IMS_7_2_MR", "IMS_7_4_1_MAIN", "IMS_7_6_CDFMC_MAIN", "IMS_7_6_CDFMC_RC", "IMS_7_6_CDFMC_RC_DROP6", "IMS_7_6_MAIN", "IMS_7_7_0", "IMS_7_7_CDFMC_MAIN", "IMS_7_7_MAIN", "IMS_7_8_MAIN", "IMS_7_4_1_CDFMC", "IMS_7_4_2_PATCH", "INTF_STAB_7_7", "MODEL_MIGRATION_7_6", "IMS_7_0_fcs_throttle", "ztna_p1")



python usm_pre_build_stats_dyn.py \
    --query_file /Users/gowe/Desktop/MyWork/SplunkDataNotification/usm_splunk_query_precommit.txt \
    --branches_file /Users/gowe/Desktop/MyWork/SplunkDataNotification/pre_branches.txt \
    --username gowe \
    --password "06AugDec1996\!@" \
    --earliest_time="-240h" \
    --latest_time="now" \
    --query_names USM_Pre_Stage_Information

working fine not send to webex



 python3 -u usm_build_statistics.py USM_Pre_Total_Builds


# python3 -u send_table_with_colored_format.py \
#   --query_file "/Users/gowe/Desktop/MyWork/SplunkDataNotification/usm_splunk_query_precommit_dynamic_values.txt" \
#   --branches_file "/Users/gowe/Desktop/MyWork/SplunkDataNotification/pre_branches.txt" \
#   --username "gowe" \
#   --password "06AugDec1996\!@" \
#   --earliest_time="-48h" \
#   --latest_time="now" \
#   --query_names "USM_Pre_Stage_Information"