#[derive(Debug, PartialEq, Eq)]
pub struct IssueTitle<'a> {
    pub prefix: Option<&'a str>,
    pub content: String,
}

pub struct Issue<'a> {
    pub title: IssueTitle<'a>,
}

pub struct RemoteIssue<'a> {
    pub title: IssueTitle<'a>,
    pub entity_id: String,
    pub description: String,
}
