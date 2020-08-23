import dash_bootstrap_components as dbc
def Navbar():
    navbar = dbc.NavbarSimple(
           children=[
              dbc.NavItem(dbc.NavLink("HOME ",active=True, href="/home",style={'color': 'blue','font-family':'Bahnschrift', 'fontSize': 25})),
              dbc.NavItem(dbc.NavLink("TRENDS ",active=True, href="/time-series",style={'color': 'blue','font-family':'Bahnschrift', 'fontSize': 25})),
              dbc.NavItem(dbc.NavLink("PREDICTIONS ",active=True, href="/time-series1",style={'color': 'blue','font-family':'Bahnschrift', 'fontSize': 25})),
              dbc.NavItem(dbc.NavLink("RESOURCES ",active=True, href="/time-series2",style={'color': 'blue','font-family':'Bahnschrift', 'fontSize': 25}))
             ],
          #brand="Home",
          #brand_href="/home",
          #sticky="top",
        )
    return navbar
