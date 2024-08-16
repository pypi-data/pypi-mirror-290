terraform {
  backend "gcs" {
  }
}

module "module_state_gcs" {
  source = "../../modules/module-state-gcs"
}
