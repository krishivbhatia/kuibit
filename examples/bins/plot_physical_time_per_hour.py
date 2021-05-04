#!/usr/bin/env python3

# Copyright (C) 2021 Gabriele Bozzola
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, see <https://www.gnu.org/licenses/>.

import logging

import matplotlib.pyplot as plt

from kuibit import argparse_helper as kah
from kuibit.simdir import SimDir
from kuibit.visualize_matplotlib import (
    get_figname,
    save_from_dir_filename_ext,
    setup_matplotlib,
)

if __name__ == "__main__":
    setup_matplotlib()

    desc = f"""\
{kah.get_program_name()} plots how much physical time is being simulated per
wall-time hour and day."""

    parser = kah.init_argparse(desc)
    kah.add_figure_to_parser(parser)

    args = kah.get_args(parser)

    # Parse arguments

    logger = logging.getLogger(__name__)

    if args.verbose:
        logging.basicConfig(format="%(asctime)s - %(message)s")
        logger.setLevel(logging.DEBUG)

    figname = get_figname(args, default="physical_time_per_hour")
    logger.debug(f"Using figname {figname}")

    sim = SimDir(args.datadir, ignore_symlinks=args.ignore_symlinks)
    logger.debug("Prepared SimDir")

    if "physical_time_per_hour" not in sim.ts.scalar:
        raise ValueError("physical_time_per_hour not available")

    phys_time = sim.ts.scalar["physical_time_per_hour"]

    logger.debug("Plotting physical_time_per_hour")

    plt.plot(phys_time)
    plt.xlabel("Simulation Time")
    plt.ylabel("Simulated physical time per hour")

    # Adding a second y axis
    plt.twinx()
    plt.plot(phys_time * 24)
    plt.ylabel(r"Simulated physical time per day")
    logger.debug("Plotted")

    logger.debug("Saving")
    save_from_dir_filename_ext(args.outdir, figname, args.fig_extension)
    logger.debug("DONE")
