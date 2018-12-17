*** Keywords ***

I select five stars
    Click Element       //*[@id="rate-form"]/div[1]/div/a[5]
    Element Should Be Enabled       //*[@id="rate-form"]/button

I select two stars
    Click Element       //*[@id="rate-form"]/div[1]/div/a[2]
    Element Should Contains     //*[@id="rating-my-service"]/div/div/div    We are sorry to hear that! 

I select one star
    Click Element       //*[@id="rate-form"]/div[1]/div/a[1]
    Element Should Contains     //*[@id="rating-my-service"]/div/div/div    We are sorry to hear that! 
