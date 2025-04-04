import { createTheme } from '@mui/material/styles';
import { config } from '../config';

export const theme = createTheme({
  palette: {
    primary: {
      main: config.app.theme.primary,
    },
    secondary: {
      main: config.app.theme.secondary,
    },
    background: {
      default: config.app.theme.background,
    },
  },
  typography: {
    fontFamily: '"Noto Sans SC", "Roboto", "Helvetica", "Arial", sans-serif',
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
        },
      },
    },
  },
});
