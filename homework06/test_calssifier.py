from string import punctuation

from bayes import NaiveBayesClassifier


def read_sms_data():
    with open('data/SMSSpamCollection', 'r', encoding="utf-8") as f:
        lines = f.readlines()
    X = [line.split('\t')[1] for line in lines]
    y = [line.split('\t')[0] for line in lines]
    return X, y


def clean_data(X, y):
    X = [i.replace('\n', '') for i in X]
    X = [i.lower() for i in X]
    X = [i.split(' ') for i in X]
    X = [[word for word in i if word not in punctuation] for i in X]
    y = [1 if i == 'spam' else 0 for i in y]
    return X, y


def split_data(X, y):
    X_train = X[:int(len(X) * 0.7)]
    y_train = y[:int(len(y) * 0.7)]
    X_test = X[int(len(X) * 0.7):]
    y_test = y[int(len(y) * 0.7):]
    return X_train, y_train, X_test, y_test


def main():
    X, y = read_sms_data()
    X, y = clean_data(X, y)
    X_train, y_train, X_test, y_test = split_data(X, y)
    bayes = NaiveBayesClassifier(alpha=0.05)
    bayes.fit(X_train, y_train)
    print(bayes.score(X_test, y_test))


if __name__ == '__main__':
    main()
