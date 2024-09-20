from View.main_view import MainView
from ViewModel.main_viewmodel import MainViewModel

if __name__ == "__main__":
    viewmodel = MainViewModel()
    view = MainView(viewmodel)
    view.run()

