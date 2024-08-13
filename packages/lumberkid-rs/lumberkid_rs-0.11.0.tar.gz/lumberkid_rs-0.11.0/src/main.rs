use clap::{Parser, Subcommand};
use commands::{rapid_add, ready};
mod commands;
mod forge;
mod issue;
mod shell_utils;

#[derive(Parser)]
#[command(version, about, long_about = None)]
struct LumberkidCLI {
    /// Turn debugging information on
    #[arg(short, long, action = clap::ArgAction::Count)]
    debug: u8,

    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand)]
pub enum Commands {
    /// Add a new item without querying the issue provider
    #[command(alias = "n")]
    New,
    /// Mark a change as ready, based on the config
    #[command(alias = "r")]
    Ready,
}

fn main() {
    let cli = LumberkidCLI::parse();

    // You can check for the existence of subcommands, and if found use their
    // matches just as you would the top level cmd
    // TODO: Get args from config
    let forge = forge::GitHub {};
    match &cli.command {
        Some(Commands::New) => rapid_add(true, "main", false, &forge).unwrap(),
        Some(Commands::Ready) => ready(&forge).unwrap(),
        None => {}
    }
}
