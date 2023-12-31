import platform
import sys

import click
import pandas as pd
import psutil

from xkr import __version__
from xkr.main import system_data_usage, interface_data_usage, process_data_usage

def version_msg():
    os = platform.system().lower()
    return f'xeeker version xkr{__version__} {os}'


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(__version__, '-V', '--version', message=version_msg())
@click.argument('command')
@click.option('-pid', '--process', is_flag=True, required=False, help='The process id')
@click.option('-i', '--interface', is_flag=True, required=False, help='The network interface')
@click.option('-p', '--period', default='daily', help='The data usage period of time')
def main(command, process, interface, period):
    if not command or command.lower() != "usage":
        click.echo(click.get_current_context().get_help())
        sys.exit(0)

    if process:
        if not process.isnumeric() or not psutil.pid_exists(int(process)):
            click.echo(f"Process ID '{process}' does not exist in current running processes")
            sys.exit(0)
        click.echo(process_data_usage(period))
        return

    if interface:
        data = interface_data_usage(period, interface)
        df = pd.DataFrame(data)
        click.echo(df.to_string())
        return

    total, download, upload = system_data_usage(period)
    click.echo(f"Total: {total}          "
            f"Download: {download}          "
            f"Upload: {upload}")


if __name__ == "__main__":
    main()
