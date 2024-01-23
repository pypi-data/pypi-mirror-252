from typing import Dict, Any

from matplotlib import pyplot as plt
import shap
import numpy as np

shap_plot_function_mapping = {"WATERFALL": shap.plots.waterfall}
plt_plot_function_mapping = {"PLOT": plt.plot, "BAR": plt.bar}


def create_plot(plot_data_dict: Dict[str, Any]) -> None:
    plot_library = plot_data_dict["plot_library"]
    plot_content = plot_data_dict["plot_content"]

    for individual_plot in plot_content:
        plot_type = individual_plot["plot_type"]
        kwargs = individual_plot["plot_data"]

        if plot_library == "SHAP":
            shap_values = shap._explanation.Explanation(
                values=np.array(kwargs["values"]),
                base_values=kwargs["base_value"],
                data=np.array(kwargs["data"]),
                feature_names=kwargs["feature_names"],
            )

            shap_plot_function_mapping[plot_type](shap_values, show=False)

        elif plot_library == "PLT":
            plt_plot_function_mapping[plot_type](**kwargs)
        else:
            raise ValueError(f"Unknown plot library {plot_library}")
