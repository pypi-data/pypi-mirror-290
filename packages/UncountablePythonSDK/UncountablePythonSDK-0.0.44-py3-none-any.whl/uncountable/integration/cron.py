from dataclasses import dataclass

from pkgs.argument_parser import CachedParser
from uncountable.integration.construct_client import construct_uncountable_client
from uncountable.integration.executors.executors import resolve_executor
from uncountable.integration.job import CronJobArguments, JobLogger
from uncountable.types.job_definition_t import JobDefinition, ProfileMetadata


@dataclass
class CronJobArgs:
    definition: JobDefinition
    profile_metadata: ProfileMetadata


cron_args_parser = CachedParser(CronJobArgs)


def cron_job_executor(**kwargs: dict) -> None:
    args_passed = cron_args_parser.parse_storage(kwargs)
    args = CronJobArguments(
        job_definition=args_passed.definition,
        client=construct_uncountable_client(profile_meta=args_passed.profile_metadata),
        profile_metadata=args_passed.profile_metadata,
        logger=JobLogger(
            profile_metadata=args_passed.profile_metadata,
            job_definition=args_passed.definition,
        ),
    )

    job = resolve_executor(args_passed.definition.executor, args_passed.profile_metadata)

    print(f"running job {args_passed.definition.name}")

    job.run(args=args)
