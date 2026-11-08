terraform {
  backend "s3" {
    bucket       = "grocerymate-tfstate-683554602189-euc1-20261108"
    key          = "grocerymate/mvp/terraform.tfstate"
    region       = "eu-central-1"
    encrypt      = true
    use_lockfile = true
  }
}
