# 用例与本轮结果

本轮：17项在线、17项离线；参数化展开，非断言数量。

| 用例 | 类型 | 结果 |
|---|---|---|
| tests/test_boundaries.py::test_denied_write_preserves_record[PATCH-False] | live | passed |
| tests/test_boundaries.py::test_denied_write_preserves_record[DELETE-False] | live | passed |
| tests/test_boundaries.py::test_denied_write_preserves_record[PUT-True] | live | passed |
| tests/test_boundaries.py::test_filter_contains_created_booking[fields0] | live | passed |
| tests/test_boundaries.py::test_filter_contains_created_booking[fields1] | live | passed |
| tests/test_boundaries.py::test_valid_boundary_values_persist[totalprice-0] | live | passed |
| tests/test_boundaries.py::test_valid_boundary_values_persist[depositpaid-False] | live | passed |
| tests/test_boundaries.py::test_valid_boundary_values_persist[additionalneeds-] | live | passed |
| tests/test_lifecycle.py::test_create_read_roundtrip | live | passed |
| tests/test_lifecycle.py::test_full_update | live | passed |
| tests/test_lifecycle.py::test_partial_update | live | passed |
| tests/test_lifecycle.py::test_unauthorized_update_preserves_data | live | passed |
| tests/test_lifecycle.py::test_delete_then_not_found | live | passed |
| tests/test_local.py::test_valid_contract | offline | passed |
| tests/test_local.py::test_invalid_field_types[firstname-1] | offline | passed |
| tests/test_local.py::test_invalid_field_types[lastname-None] | offline | passed |
| tests/test_local.py::test_invalid_field_types[totalprice-True] | offline | passed |
| tests/test_local.py::test_invalid_field_types[totalprice-100] | offline | passed |
| tests/test_local.py::test_invalid_field_types[depositpaid-1] | offline | passed |
| tests/test_local.py::test_invalid_field_types[bookingdates-bad5] | offline | passed |
| tests/test_local.py::test_invalid_dates[2027-02-30] | offline | passed |
| tests/test_local.py::test_invalid_dates[2027/05/10] | offline | passed |
| tests/test_local.py::test_invalid_dates[invalid] | offline | passed |
| tests/test_local.py::test_invalid_dates[123] | offline | passed |
| tests/test_local.py::test_network_failure_is_distinguishable | offline | passed |
| tests/test_local.py::test_wrong_status_diagnostic | offline | passed |
| tests/test_local.py::test_invalid_json_diagnostic | offline | passed |
| tests/test_local.py::test_cleanup_checks_ownership[present] | offline | passed |
| tests/test_local.py::test_cleanup_checks_ownership[missing] | offline | passed |
| tests/test_local.py::test_cleanup_checks_ownership[changed_owner] | offline | passed |
| tests/test_readonly.py::test_list_contract | live | passed |
| tests/test_readonly.py::test_detail_contract | live | passed |
| tests/test_readonly.py::test_unknown_route | live | passed |
| tests/test_readonly.py::test_invalid_credentials | live | passed |
