terraform {
  backend "http" {
    address        = "https://gitlab.com/api/v4/projects/<PROJECT_ID>/terraform/state/play"
    lock_address   = "https://gitlab.com/api/v4/projects/<PROJECT_ID>/terraform/state/play/lock"
    unlock_address = "https://gitlab.com/api/v4/projects/<PROJECT_ID>/terraform/state/play/lock"
    lock_method    = "POST"
    unlock_method  = "DELETE"
    retry_wait_min = 5
  }
}
