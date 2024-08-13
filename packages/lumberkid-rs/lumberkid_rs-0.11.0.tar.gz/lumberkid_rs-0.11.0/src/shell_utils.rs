use std::io::Write;
use std::io::{BufRead, BufReader};
use std::process::Command;
use std::process::Stdio;
use std::thread;
use termcolor::{Color, ColorChoice, ColorSpec, StandardStream, WriteColor};

pub fn shell_out(command: &str, args: &[&str]) -> std::io::Result<()> {
    let mut child = Command::new(command)
        .args(args)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;

    let stdout = child.stdout.take().expect("Failed to capture stdout");
    let stderr = child.stderr.take().expect("Failed to capture stderr");

    let mut stdout_writer = StandardStream::stdout(ColorChoice::Always);
    let mut stderr_writer = StandardStream::stderr(ColorChoice::Always);

    let stdout_thread = thread::spawn(move || {
        let reader = BufReader::new(stdout);
        for line in reader.lines() {
            let line = line.expect("Failed to read stdout line");
            stdout_writer
                .set_color(ColorSpec::new().set_fg(Some(Color::Green)))
                .unwrap();
            writeln!(&mut stdout_writer, "{}", line).unwrap();
            stdout_writer.reset().unwrap();
        }
    });

    let stderr_thread = thread::spawn(move || {
        let reader = BufReader::new(stderr);
        for line in reader.lines() {
            let line = line.expect("Failed to read stderr line");
            stderr_writer
                .set_color(ColorSpec::new().set_fg(Some(Color::Red)))
                .unwrap();
            writeln!(&mut stderr_writer, "{}", line).unwrap();
            stderr_writer.reset().unwrap();
        }
    });

    stdout_thread.join().expect("Stdout thread panicked");
    stderr_thread.join().expect("Stderr thread panicked");

    let status = child.wait()?;
    if !status.success() {
        panic!(
            "Command '{} {}' failed with exit code: {}",
            command,
            args.join(" "),
            status
        );
    }
    Ok(())
}
