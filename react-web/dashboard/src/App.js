import React from 'react';
import './App.css';
import { makeStyles } from '@material-ui/core/styles';
import TopNavBar from './components/TopNavBar'
import DashboardPage from './pages/DashboardPage'
import { HOME_PAGE, DASHBOARD_PAGE } from './Constants';
import Cookies from 'universal-cookie';
// {
//   height: 'calc(100% - 56px)',
//   [`${theme.breakpoints.up('xs')} and (orientation: landscape)`]: {
//     height: 'calc(100% - 48px)',
//   },
//   [theme.breakpoints.up('sm')]: {
//     height: 'calc(100% - 64px)',
//   },
// },

const useStyles = makeStyles((theme) => ({
  root: {
    height: "100%"
  },
  title: {
    textAlign: 'initial',
    margin: theme.spacing(4, 0, 2),
  },
}));

// const toolbarRelativeProperties = (property, modifier = value => value) => theme =>
//   Object.keys(theme.mixins.toolbar).reduce((style, key) => {
//     const value = theme.mixins.toolbar[key];
//     if (key === 'minHeight') {
//       return { ...style, [property]: modifier(value) };
//     }
//     if (value.minHeight !== undefined) {
//       return { ...style, [key]: { [property]: modifier(value.minHeight) } };
//     }
//     return style;
//   }, {});

function App() {
  const classes = useStyles();
  // Try to get user data from cookies
  const cookies = new Cookies();
  const [userData, setUserData] = React.useState({
    userId: cookies.get('userId'),
    userName: cookies.get('userName'),
    userEmail: cookies.get('userEmail'),
  });

  const [currentPage, switchPage] = React.useState(HOME_PAGE);

  // React.useEffect(() => {
  //   if (userData.userId == undefined) {
  //     window.location.pathname = './login';
  //   }
  // }, [userData]);

  return (
    <div className={classes.root}>
      <TopNavBar 
        userData={userData} 
        setUserData={setUserData}
        switchPage={switchPage}
      />
      <DashboardPage
        userData={userData}
      />
    </div>
  );
}

export default App;
