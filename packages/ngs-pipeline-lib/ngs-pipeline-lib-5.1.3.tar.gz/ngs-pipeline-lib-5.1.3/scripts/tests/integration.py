import boto3
import structlog

from scripts import configure_logging
from scripts.tests.exceptions import TestError
from scripts.tests.main import cli
from scripts.tests.models.integration import (
    IntegrationTestArgs,
    IntegrationTestSettings,
)
from scripts.tests.utils.common import clean_files
from scripts.tests.utils.integration import (
    compare_output_files,
    get_test_container_output_files,
    get_test_scenarios,
    import_expected_output_files,
    import_remote_input_files,
    run_test_container,
)

logger = structlog.getLogger("ngs-test")


@cli.command()
def integration(args: IntegrationTestArgs):
    run_settings = IntegrationTestSettings()
    configure_logging(
        verbose=run_settings.verbose,
        json=run_settings.json_logger,
        log_file_path=run_settings.log_file,
    )

    scenarios = get_test_scenarios(
        run_settings=run_settings, name_filters=args.name_filter
    )

    scenarios_count = len(scenarios)
    logger.info(f"Configuration used : {run_settings}")
    logger.info(f"Found {scenarios_count} scenario(s)")
    for scenario in scenarios:
        logger.info(f"\t{scenario.scenario.name}")

    logger.info(f"Setting Default AWS Profile to {run_settings.aws_profile}")
    boto3.setup_default_session(profile_name=run_settings.aws_profile)

    logger.info(
        f"Creating Output folder if needed : {str(run_settings.test_output_folder)}"
    )
    run_settings.test_output_folder.mkdir(parents=True, exist_ok=True)

    if args.clean_cache:
        logger.info(f"Cleaning cache folder {args.cache_folder}")
        clean_files(path=args.cache_folder)

    failure_count = error_count = 0
    for scenario in scenarios:
        logger.info("-" * 150)
        logger.info(f"Running test {scenario.scenario.name}")

        scenario_output_folder = (
            run_settings.test_output_folder / scenario.scenario.name.replace(" ", "-")
        )
        scenario_input_folder = (
            run_settings.test_local_input_folder
            / scenario.scenario.name.replace(" ", "-")
        )
        scenario_output_folder.mkdir(parents=True, exist_ok=True)
        scenario_input_folder.mkdir(parents=True, exist_ok=True)

        clean_files(path=scenario_output_folder)
        clean_files(path=scenario_input_folder)

        try:
            local_input_files = import_remote_input_files(
                test=scenario,
                destination_folder=scenario_input_folder,
                root_cache_folder=args.cache_folder,
                use_cache=args.use_cache,
            )

            for key, file in local_input_files.items():
                scenario.inputs[key] = str(file)

            test_container = run_test_container(
                test=scenario, run_settings=run_settings
            )

            get_test_container_output_files(
                container=test_container,
                test_configuration=scenario,
                output_folder=scenario_output_folder,
            )

            import_expected_output_files(
                test_configuration=scenario,
                scenario_path=scenario.scenario.path,
                output_folder=scenario_output_folder,
            )
            compare_output_files(
                test_configuration=scenario,
                output_folder=scenario_output_folder,
            )  # raises TestError in case of discrepancies

            if args.post_clean:
                logger.info("\tCleaning scenario input and output folders")
                clean_files(path=scenario_output_folder)
                clean_files(path=scenario_input_folder)

            logger.info("\tTest OK")
        except TestError as e:
            logger.info(f"\tTest failed. Reason: {e}")
            failure_count += 1
        except Exception:
            logger.exception("\tERROR while running test.")
            error_count += 1

    logger.info("-" * 150)
    logger.info(
        f"Tests finished. {scenarios_count - failure_count - error_count}/{scenarios_count} passed"
    )
    if failure_count > 0:
        logger.info(f"Tests failures : {failure_count}")
    if error_count > 0:
        logger.info(f"Tests errors : {error_count}")
