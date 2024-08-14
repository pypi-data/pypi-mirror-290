module "error_notifications_virginia" {
  providers = {
    aws = aws.us-east-1
  }
  source   = "git::https://github.com/miquido/sns-notifications.git?ref=tags/1.0.4"

  environment = var.environment
  project     = var.project
  webhooks    = [var.gchat_webhook]
}

module "error_notifications" {
  source   = "git::https://github.com/miquido/sns-notifications.git?ref=tags/1.0.4"

  environment = var.environment
  project     = var.project
  webhooks    = [var.gchat_webhook]
}
