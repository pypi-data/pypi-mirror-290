from benvy.databricks.repos.config.BootstrapConfig import BootstrapConfig
from benvy.container.dicontainer import Container


class BootstrapInstallConfig(BootstrapConfig):
    def get_setup_steps(self, container: Container):
        return [
            container.get_dbx_poetry_downloader(),
            container.get_dbx_poetry_install_script_downloader(),
            container.get_dbx_poetry_installer(),
            container.get_dbx_dbr_python_checker(),
            container.get_dbx_dbr_dependencies_checker(),
            container.get_dbx_package_installer(),
        ]
