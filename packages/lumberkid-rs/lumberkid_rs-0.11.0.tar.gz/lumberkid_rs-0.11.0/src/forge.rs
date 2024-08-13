use core::fmt;

use crate::{issue::Issue, shell_utils::shell_out};

#[derive(Debug)]
pub enum MergeMethod {
    Merge,
    Rebase,
    Squash,
}

impl fmt::Display for MergeMethod {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            MergeMethod::Merge => write!(f, "merge"),
            MergeMethod::Rebase => write!(f, "rebase"),
            MergeMethod::Squash => write!(f, "squash"),
        }
    }
}

pub trait Forge {
    fn setup(&self);
    fn begin(&self, issue: Issue, start_as_draft: bool) -> Result<(), std::io::Error>;
    fn ready(&self, automerge: bool, merge_method: MergeMethod, mark_as_ready: bool);
}

// Implement for GitHub
pub struct GitHub {}

impl Forge for GitHub {
    fn setup(&self) {}

    fn begin(
        &self,
        issue: Issue,
        start_as_draft: bool,
        // TODO: title_formatter: impl Fn(&Issue) -> String,
    ) -> Result<(), std::io::Error> {
        self.setup();

        let pr_title = pr_title(&issue);
        let mut args = vec!["pr", "create", "--title", &pr_title, "--body", ""];

        if start_as_draft {
            args.push("--draft");
        }
        shell_out("gh", &args)
    }

    fn ready(&self, automerge: bool, merge_method: MergeMethod, mark_as_ready: bool) {
        self.setup();
        if mark_as_ready {
            let _ = shell_out("gh", &["pr", "ready"]);
        }

        let mut merge_cmd = vec!["pr", "merge"];
        if automerge {
            merge_cmd.push("--auto");
        }
        match merge_method {
            MergeMethod::Merge => merge_cmd.push("--merge"),
            MergeMethod::Rebase => merge_cmd.push("--rebase"),
            MergeMethod::Squash => merge_cmd.push("--squash"),
        }

        let _ = shell_out("gh", &merge_cmd);
    }
}

fn pr_title(issue: &Issue) -> String {
    match issue.title.prefix {
        Some(ref prefix) => format!("{}: {}", prefix, issue.title.content),
        None => issue.title.content.to_string(),
    }
}
